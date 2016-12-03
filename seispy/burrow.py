from gazelle.datascope import closing,\
                              dbopen
import seispy.station
from seispy.util import validate_time
from obspy.core import read,\
                       Stream
import os
import shutil
import subprocess
import tempfile

class Groundhog:
    def __init__(self,
                 server_directory="rsync://eqinfo.ucsd.edu/ANZA_waveforms",
                 database_dir="/home/seismech-00/sjfzdb/anf/wfdiscs"):
        self.server_directory = server_directory
        self.dbs = {}
        self.wfdiscs = {}
        for year in range(1998, 2016):
            self.dbs[year] = dbopen(os.path.join(database_dir, str(year)))
        self.temp_dir = tempfile.mkdtemp()

    def __del__(self):
        for year in self.dbs:
            self.dbs[year].close()
        shutil.rmtree(self.temp_dir)

    def fetch(self, station, channel, starttime, endtime):
        """
        Fetch waveform data from ANF rsync server at UCSD.
        """
        starttime = validate_time(starttime)
        endtime = validate_time(endtime)
        if isinstance(station, seispy.station.Station):
            station = station.name
        if isinstance(station, seispy.station.Channel):
            channel = channel.code
        if not starttime.year == endtime.year:
            raise NotImplementedError
        tbl_wfdisc = self.dbs[starttime.year].lookup(table="wfdisc")
        view = tbl_wfdisc.subset("sta =~ /%s/ && chan =~ /%s/ && endtime > _%f_"
                                 "&& time < _%f_" % (station,
                                                     channel,
                                                     starttime.timestamp,
                                                     endtime.timestamp))
        view_unique = view.sort(("sta", "chan"), unique=True)
        st = Stream()
        for control_record in view_unique.iter_record():
            sta, chan = control_record.getv("sta", "chan")
            view_data = view.subset("sta =~ /%s/ && chan =~ /%s/ && endtime"
                                    "> _%f_ && time < _%f_" %(sta,
                                                              chan,
                                                              starttime.timestamp,
                                                              endtime.timestamp))
            for data_record in view_data.iter_record():
                ddir, dfile = data_record.getv("dir", "dfile")
                with open(os.devnull, 'w') as FNULL:
                    subprocess.call(["rsync",
                                     "-a",
                                     "-v",
                                     "-P",
                                     "--whole-file",
                                     "%s/%s/%s" % (self.server_directory,
                                                   ddir,
                                                   dfile),
                                     self.temp_dir],
                                     stdout=FNULL)
                os.listdir(self.temp_dir)
                st += read(os.path.join(self.temp_dir, dfile))
                os.remove(os.path.join(self.temp_dir, dfile))
        st.trim(starttime, endtime)
        return st

if __name__ == "__main__":
    willy = Groundhog("rsync://eqinfo.ucsd.edu/ANZA_waveforms")
    st = willy.fetch("PFO", "HHZ", validate_time("2015-120T00:00:00"), validate_time("2015-120T00:01:00"))
    st.plot()