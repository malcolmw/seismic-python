import seispy as sp
import matplotlib.pyplot as plt
import numpy as np
import obspy
import scipy

logger = sp.log.initialize_logging(__name__)


class Trace(obspy.core.Trace):
    """
    ... todo::
        document this class
    """
    def __init__(self, *args):
        """
        Trace objects can be initialized by one of two call signatures:
        Trace(database, station, channel, starttime, endtime)
        OR
        Trace(wffile)
        """
        if len(args) == 5:
            self.__init_from_db(*args)
        elif len(args) == 1:
            self.__init_from_wffile(*args)

    def __init_from_db(self, database, station, channel, starttime, endtime):
        starttime = sp.util.validate_time(starttime)
        endtime = sp.util.validate_time(endtime)
        if isinstance(station, sp.station.Station):
            sta = station.name
        else:
            sta = station
        if isinstance(channel, sp.station.Channel):
            chan = channel.code
        else:
            chan = channel
        try:
            groupd = database.wfdisc["grouped"]
            groupd.record = groupd.find("sta =~ /%s/ && chan =~ /%s/"
                                        % (sta, chan))
        except Exception:
            raise IOError("data not found")
        rnge = groupd.get_range()
        sortd = database.wfdisc["sorted"]
        view = sortd.list2subset(range(rnge[0], rnge[1]))
        _tmp = view.subset("endtime > _%f_ && time < _%f_"
                           % (starttime.timestamp, endtime.timestamp))
        view.free()
        view = _tmp
        st = obspy.core.Stream()
        for record in view.iter_record():
            st += obspy.core.read(record.filename()[1],
                                  starttime=starttime,
                                  endtime=endtime)[0]
        view.free()
        st.merge()
        tr = st[0]
        self.stats = tr.stats
        self.stats.station = station
        self.stats.channel = channel
        self.data = tr.data

    def __init_from_wffile(self, *args):
        tr = obspy.core.read(*args)[0]
        self.stats = tr.stats
        self.data = tr.data

    def filter(self, *args, **kwargs):
        self.trim(starttime=self.stats.starttime - 10,
                  pad=True,
                  fill_value=int(self.data.mean()))
        super(self.__class__, self).filter(*args, **kwargs)
        self.trim(starttime=self.stats.starttime + 10)

    def pick_fzhw(self, params=None):
        """
        This method attempts to pick fault-zone head-waves.
        """
        # Parse input parameter dictionary, using default parameters
        # where necessary.
        default_params = {"sta_twin": 0.1,
                          "lta_twin": 10.0,
                          "stalta_thresh_on": 10,
                          "stalta_thresh_off": 4,
                          "kurtosis_thresh_on": 5,
                          "kurtosis_thresh_off": 2,
                          "kurtosis_twin": 5,
                          "skewness_thresh_on": 3,
                          "skewness_thresh_off": 0.5,
                          "skewness_twin": 5}
        if params is None:
            params = default_params
        else:
            for key in default_params:
                if key not in params:
                    params[key] = default_params[key]
        # Do any waveform pre-processing here.
        #
        #
        # Relabel some variables for convenience
        sr = self.stats.sampling_rate
        dt = self.stats.delta
        kt = params["kurtosis_twin"]
        st = params["skewness_twin"]
        MAGIC_NUMBER = 0.03
        trigger_onset = obspy.signal.trigger.trigger_onset
        # Now make a first pick attempt from the STA/LTA.
        cft = self.copy()
        cft.trigger("recstalta",
                    sta=params["sta_twin"],
                    lta=params["lta_twin"])
        try:
            triggers = trigger_onset(cft.data,
                                     params["stalta_thresh_on"],
                                     params["stalta_thresh_off"])
        except Exception as err:
            logger.error(err)
            raise
        # We want the onset time of the maximum value of the STA/LTA
        try:
            cft_max = max([max(cft.data[sample_on:sample_off])
                           for sample_on, sample_off in triggers])
        except ValueError as err:
            logger.warning("STA/LTA threshold not exceeded")
            raise
        cft_sample_on = cft.data.tolist().index(cft_max)
        cft_alternate = triggers[0][0]
        # cft_min = min(cft.data[cft_sample_on-int(MAGIC_NUMBER*sr):cft_sample_on])
        # cft_alternate = cft.data.tolist().index(cft_min)
        # Now make a pick from the kurtosis time series
        # Calculate kurtosis time series
        kcft = np.absolute([scipy.stats.kurtosis(self.data[i:i+int(kt*sr)])
                           for i in range(int(self.stats.npts-kt*sr))])
        triggers = trigger_onset(kcft,
                                 params["kurtosis_thresh_on"],
                                 params["kurtosis_thresh_off"])
        # We want the onset time of the maximum value of the kurtosis
        # time series
        try:
            kcft_max = max([max(kcft[sample_on:sample_off])
                            for sample_on, sample_off in triggers])
        except ValueError as err:
            logger.warning("kurtosis threshold not exceeded")
            raise
        # When retrieving the sample index of the maximum kurtosis
        # value, left-shift the index by the length of the kurtosis
        # time window to treat things causally.
        kcft_sample_on = kcft.tolist().index(kcft_max) +\
            int(params["kurtosis_twin"] * sr)
        #
        #
        # Zach refines picks using the derivative of kurtosis here!
        #
        #
        # Now make a pick from the skewness time series
        # Calculate skewness time series
        scft = np.absolute([scipy.stats.skew(self.data[i:i+int(st*sr)])
                           for i in range(int(self.stats.npts-st*sr))])
        triggers = trigger_onset(scft,
                                 params["skewness_thresh_on"],
                                 params["skewness_thresh_off"])
        # We want the onset time of the maximum value of the skewness
        # time series
        try:
            scft_max = max([max(scft[sample_on:sample_off])
                            for sample_on, sample_off in triggers])
        except ValueError as err:
            logger.warning("skewness threshold not exceeded")
            raise
        # When retrieving the sample index of the maximum skewness
        # value, left-shift the index by the length of the skewness
        # time window to treat things causally.
        scft_sample_on = scft.tolist().index(scft_max) +\
            int(params["skewness_twin"] * sr)
        #
        #
        # Zach refines picks using the derivative of skewness here!
        #
        #
        # Zach also does an additional check to see if the average of
        # the skewness and kurtosis picks is less than the STA/LTA
        # pick, returning only the STA/LTA pick if it is.
        #
        #
        # Then Zach does a series of checks for polarity flips.
        #
        #
        # Now a check to verify that head-wave pick is within
        # appropriate neighbourhood of P-wave pick.
        st = obspy.core.Stream(traces=[self, cft])
        fig = st.plot(handle=True, equal_scale=False)
        ax = fig.axes[0]
        ts = self.stats.starttime
        p = ts.toordinal() +\
            ts._get_hours_after_midnight() / 24. +\
            cft_sample_on * dt / 86400.
        ax.axvline(p)
        p = ts.toordinal() +\
            ts._get_hours_after_midnight() / 24. +\
            cft_alternate * dt / 86400.
        ax.axvline(p)
        plt.show()
        ts = self.stats.starttime + cft_alternate * dt - 1
        te = self.stats.starttime + cft_sample_on * dt + 1
        self.trim(starttime=ts, endtime=te)
#        plt.figure()
#        plt.plot(self.data, "k")
#        plt.vlines(sr, max(self.data), min(self.data), color="r")
#        plt.vlines(self.stats.npts - sr,
#                   max(self.data),
#                   min(self.data), color="b")
#        plt.show()
        return cft_sample_on, cft_alternate, kcft_sample_on, scft_sample_on


class Trace_dep(obspy.core.Trace):
    """
    .. todo::
       document this class
    """        
    def plot(self,
             starttime=None,
             endtime=None,
             arrivals=None,
             detections=None,
             show=True,
             xticklabel_fmt=None):
        fig = plt.figure(figsize=(12, 3))
        ax = fig.add_subplot(1, 1, 1)
        ax = self.subplot(ax,
                          starttime=starttime,
                          endtime=endtime,
                          arrivals=arrivals,
                          detections=detections,
                          xticklabel_fmt=xticklabel_fmt)
        if show:
            plt.show()
        else:
            return fig

    def subplot(self,
                ax,
                starttime=None,
                endtime=None,
                arrivals=None,
                detections=None,
                xaxis_set_visible=True,
                xticklabel_fmt=None,
                set_xlabel=True,
                set_xticks_label=None,
                set_yticks_position=None,
                label=False):
        if xticklabel_fmt == None:
            xticklabel_fmt = "%Y%j %H:%M:%S.%f"
        starttime = float(starttime) if starttime else float(self.stats.starttime)
        first_sample = int(round((starttime - float(self.stats.starttime)) / self.stats.delta))
        endtime = float(endtime) if endtime else float(self.stats.endtime)
        npts = int((endtime - starttime) / self.stats.delta)
        time = [(starttime + i * self.stats.delta) for i in range(npts)]
        x_range = endtime - starttime
        y_range = max(self.data[first_sample:npts]) -\
                    min(self.data[first_sample:npts])
        ax.plot(time, self.data[first_sample:npts], 'k')
        # Configure the x-axis.
        ax.set_xlim([float(self.stats.starttime), float(self.stats.endtime)])
        if not xaxis_set_visible:
            ax.xaxis.set_visible(False)
        if xaxis_set_visible and set_xticks_label:
            ax.set_xticklabels([sp.util.validate_time(t).strftime(xticklabel_fmt)\
                                for t in ax.get_xticks()],
                               rotation=10,
                               horizontalalignment='right')
        if set_xlabel:
            stime = sp.util.validate_time(starttime).strftime("%Y%j")
            etime = sp.util.validate_time(endtime).strftime("%Y%j")
            if stime == etime:
                ax.set_xlabel(stime, fontsize=16)
            else:
                ax.set_xlabel("%s - %s" % (stime, etime),
                              fontsize=16)
        # Configure the y-axis.
        if hasattr(self.stats.station, "name"):
            station = self.stats.station.name
        else:
            station = self.stats.station
        if hasattr(self.stats.channel, "code"):
            channel = self.stats.channel.code
        else:
            channel = self.stats.channel
        ax.text(0.5, 0.5,
                "%s:%s" % (station, channel))
        if set_yticks_position:
            ax.yaxis.set_ticks_position(set_yticks_position)
        trmax = max([abs(min(self.data)), abs(max(self.data))])
        ax.set_ylim([-trmax * 1.1, trmax * 1.1])
        ax.set_yticks([int(round(-trmax / 2.)),
                       0, 
                       int(round(trmax / 2.))])
        if arrivals: [ax.axvline(x=arrival.time,
                                 ymin=0.1,
                                 ymax=0.9,
                                 color='r',
                                 linewidth=2)\
                      for arrival in arrivals]
        if detections: [ax.axvline(x=detection.time,
                                   ymin=0.1,
                                   ymax=0.9,
                                   color='b',
                                   linewidth=2,
                                   linestyle="--")\
                        for detection in detections]
        return ax

    def noise_pad(self, twin, noise_twin=0):
        if noise_twin == 0:
            #Draw random noise.
            pass
            return
        noise = self.data[:noise_twin * self.stats.sampling_rate]
        npad_samples= twin * self.stats.sampling_rate
        self.trim(starttime=self.stats.starttime - twin, pad=True, fill_value=0.0)
        self.data[:npad_samples] = np.random.choice(noise, size=npad_samples, replace=True)


def test():
    for file in ("SOL.HHZ.2016.271.00.00.00",
                 "i4.LMS.HHZ.2016271_0+",
                 "20160927000000.CI.GMR.HHZ.mseed"):
        tr = Trace("/home/seismech-00/sjfzdb/continuous_wfs_tmp/2016/271/%s" % file)
        tr.filter("highpass", freq=0.5, corners=2, zerophase=True)
        ts = sp.util.validate_time("2016271T03:36:25")
        tr.trim(starttime=ts, endtime=ts+30)
        tr.pick_fzhw()
    
if __name__ == "__main__":
    test()
