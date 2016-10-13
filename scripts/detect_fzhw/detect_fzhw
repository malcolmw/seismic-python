#!/usr/bin/env python

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
import glob
import os
from obspy.signal.trigger import triggerOnset as trigger_onset
from gazelle.datascope import Database
from seispy.core import Trace
from seispy.geometry import hypocentral_distance
from seispy.util import MultiThreadProcess

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("database", type=str, help="database")
    parser.add_argument("cfg_file", type=str, help="config file")
    return parser.parse_args()

def parse_cfg(args):
    cfg = {}
    config = RawConfigParser()
    config.read(args.cfg_file)
    cfg["waveform_directory"] = config.get("General", "waveform_directory")
    cfg["file_match"] = config.get("General", "file_match")
    cfg["n_threads"] = config.getint("General", "n_threads")
    cfg["maximum_velocity_contrast"] = config.getfloat("Algorithm Parameters",
                                                        "maximum_velocity_contrast")
    cfg["minimum_distance_allowed"] = config.getfloat("Algorithm Parameters", "minimum_distance_allowed")
    cfg["high_pass_corner_frequency"] = config.getfloat("Algorithm Parameters", "high_pass_corner_frequency")
    cfg["require_polarity_reversal"] = config.getboolean("Algorithm Parameters", "require_polarity_reversal")
    cfg["sta_twin"] = config.getfloat("Algorithm Parameters", "sta_twin")
    cfg["lta_twin"] = config.getfloat("Algorithm Parameters", "lta_twin")
    cfg["minimum_time_separation"] = config.getfloat("Algorithm Parameters", "minimum_time_separation")
    cfg["Vp_fast"] = config.getfloat("Algorithm Parameters", "Vp_fast")
    cfg["kurtosis_twin"] = config.getfloat("Algorithm Parameters", "kurtosis_twin")
    cfg["fault_lat0"] = config.getfloat("Algorithm Parameters", "fault_lat0")
    cfg["fault_lon0"] = config.getfloat("Algorithm Parameters", "fault_lat0")
    cfg["fault_lat1"] = config.getfloat("Algorithm Parameters", "fault_lat0")
    cfg["fault_lon1"] = config.getfloat("Algorithm Parameters", "fault_lat0")
    return cfg

def inputter(db):
    for origin in db.iterate_events(subset="evid == 132703"):
        yield origin

def main_processor(origin, cfg, stations):
    evid, time = origin.evid, origin.time
    for wf_file in glob.glob(os.path.join(cfg["waveform_directory"],
                                              str(time.year),
                                              str(evid),
                                              cfg["file_match"])):
        tr = Trace(wf_file)
        station = stations[str(tr.stats.station)]
        hypo_dist = hypocentral_distance(station.lat, station.lon, -station.elev,
                                         origin.lat, origin.lon, origin.depth)
        if hypo_dist < cfg["minimum_distance_allowed"]:
            continue
        tr.detrend('linear')
        print trigger_onset(tr.trigger("classicstalta", sta=1, lta=10).data, 5, 2.5)
        tr.plot()
        if tr.stats.channel[1] == 'N':
            tr.integrate()
            tr.detrend('linear')
            tr.integrate()
            #tr.filter("highpass", freq=cfg["high_pass_corner_frequency"])
        print "processing", wf_file
        detections = tr.pick_fzhw()
        if detections:
            #tr.trim(starttime=detections[0].time - 1, endtime=detections[0].time + 1)
            tr.plot(detections=detections)

def outputter(detection):
    pass

def main():
    args = parse_args()
    cfg = parse_cfg(args)
    database = Database(args.database)
    stations = database.parse_network("YN").stations
    extra_args = {'input_init_args': (database,),
                  'main_init_args': (cfg, stations)}
    config_params = {'n_threads': cfg["n_threads"]}
    mtp = MultiThreadProcess(inputter,
                             main_processor,
                             outputter,
                             extra_args=extra_args,
                             config_params=config_params)
    mtp.start()
    database.close()

if __name__ == "__main__":
    main()
