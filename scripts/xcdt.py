#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 10:46:54 2016

@author: malcolcw

This is a script to calculate cross-correlation time differentials
suitable for use with HypoDD.
"""
import matplotlib.pyplot as plt
import numpy as np

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
from gazelle.datascope import Database
from seispy.util import MultiThreadProcess
from obspy.signal.cross_correlation import xcorr

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("database", type=str, help="database")
    parser.add_argument("config_file", type=str, help="config file")
    return parser.parse_args()
    
def parse_config(config_file):
    parser = RawConfigParser()
    parser.read(config_file)
    cfg = {}
    cfg["start_lead"] = parser.getfloat("General", "start_lead")
    cfg["end_lag"] = parser.getfloat("General", "end_lag")
    cfg["shift_len"] = parser.getfloat("General", "shift_len")
    return cfg

def inputter(infile):
    infile = open(infile)
    for line in infile:
        yield [int(evid) for evid in line.split()]
    infile.close()
    
def main_processor(pair, db, cfg):
    evid1, evid2 = pair
    origin1 = db.get_prefor(evid1)
    origin2 = db.get_prefor(evid2)
    if origin1.time > origin2.time:
        origin1, origin2 = origin2, origin1
    xcorrs = (pair,)
    for arrival in origin1.arrivals:
        if not (arrival.station.name == "CRY" and arrival.channel.code[2] == "Z"):
            continue
        tt = arrival.time - origin1.time
        try:
            trace1 = db.load_trace(station=arrival.station,
                                   channel=arrival.channel,
                                   starttime=arrival.time - cfg["start_lead"],
                                   endtime=arrival.time + cfg["end_lag"])
            trace2 = db.load_trace(station=arrival.station,
                                   channel=arrival.channel,
                                   starttime=origin2.time + tt - cfg["start_lead"],
                                   endtime=origin2.time + tt + cfg["end_lag"])
            trace1.filter("highpass", freq=3.0)
            trace2.filter("highpass", freq=3.0)
        except IOError:
            continue
        shift = int(cfg["shift_len"] * trace1.stats.sampling_rate)
        xc = xcorr(trace1, trace2, shift_len=shift)
        dt = float(trace2.stats.starttime)\
             + xc[0] * trace2.stats.delta\
             - float(arrival.time)
        xcorrs += ((xc[1],
                    dt,
                    arrival.station,
                    arrival.phase),)
    return xcorrs
    
def outputter(xcorrs):
    pair = xcorrs[0]
    print "# %d %d" % (pair[0], pair[1])
    for xc in xcorrs[1:]:
        print "%s\t%s\t%15.4f\t%.2f" % (xc[2].name,
                                      xc[3],
                                      xc[1],
                                      xc[0] ** 2)

def main():
    args = parse_args()
    cfg = parse_config(args.config_file)
    db = Database(args.database)
    extra_args = {"input_init_args": (args.infile,),
                  "main_init_args": (db, cfg)}
    config_params = {"n_threads": 1,
                     "input_q_max_size": 10,
                     "output_q_max_size": 10}
    mtp = MultiThreadProcess(inputter,
                             main_processor,
                             outputter,
                             extra_args=extra_args,
                             config_params=config_params)
    mtp.start()

if __name__ == "__main__":
    main()
