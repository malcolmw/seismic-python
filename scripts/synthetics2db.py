#!/usr/bin/env python
from ConfigParser import RawConfigParser
import os
import sys
sys.path.append("%s/data/python" % os.environ['ANTELOPE'])
from antelope.datascope import closing,\
                               dbopen
import numpy as np
from seispy.core import Arrival, Station

def parse_config(config_file):
    cfg, propgrid = {}, {}
    cfg_file = RawConfigParser()
    cfg_file.read(config_file)
    cfg['db'] = cfg_file.get('General', 'database')
    cfg['stations'] = cfg_file.get('General', 'stations')
    cfg['sources'] = cfg_file.get('General', 'sources')
    cfg['author'] = cfg_file.get('General', 'author')
    cfg['niter'] = cfg_file.getint('General', 'iterations_per_source')
    cfg['minsta'] = cfg_file.getint('General', 'min_stations')
    cfg['maxsta'] = cfg_file.getint('General', 'max_stations')
    return cfg

def read_stations(infile):
    stations = []
    infile = open(infile)
    for line in infile:
        name, lon, lat, elev = line.split()
        lon, lat, elev = float(lon) % 360., float(lat), float(elev)
        stations += [Station(name, lon, lat, elev)]
    return stations

def main(cfg):
    stations = read_stations(cfg['stations'])
    sourcesf = open(cfg['sources'])
    with closing(dbopen(cfg['db'], 'r+')) as db:
        tbl_origin = db.lookup(table='origin')
        tbl_event = db.lookup(table='event')
        tbl_assoc = db.lookup(table='assoc')
        tbl_arrival = db.lookup(table='arrival')
        for srcline in sourcesf:
            evid = tbl_event.nextid('evid')
            lat0, lon0, z0, t0 = [float(v) for v in srcline.split()]
            for i in range(cfg['niter']):
                orid = tbl_origin.nextid('orid')
                print "updating event:", evid, "orid:", orid, i + 1
                if i == 0:
                    tbl_event.record = tbl_event.addnull()
                    tbl_event.putv(("evid", evid),
                                   ("prefor", orid),
                                   ("auth", cfg['author']))
                tbl_origin.record = tbl_origin.addnull()
                tbl_origin.putv(("orid", orid),
                                ("evid", evid),
                                ("lat", lat0),
                                ("lon", lon0),
                                ("depth", z0),
                                ("time", float(t0)),
                                ("auth", cfg['author']))
                                
                arrivals = {'P': [], 'S': []}
                for phase in ('P', 'S'):
                    arrivalsf = open("arrivals/%s%d.dat" % (phase, evid - 1))
                    i = 0
                    for arrline in arrivalsf:
                        sta = stations[i]
                        i += 1
                        ta = t0 + float(arrline.split()[4])
                        arrivals[phase] += [Arrival(sta.name, 'ILSB', ta, phase)]
                nParr = int(np.random.random(1)[0] * (cfg['maxsta'] - cfg['minsta'])) + cfg['minsta']
                nSarr = int(np.random.random(1)[0] * nParr)
                arrivals['P'] = np.random.choice(arrivals['P'], size=nParr)
                _arrivals = []
                for arrival in arrivals['S']:
                    for arrivalP in arrivals['P']:
                        if arrival.station == arrivalP.station:
                            _arrivals += [arrival]
                if nSarr > 0:
                    arrivals['S'] = np.random.choice(_arrivals, size=nSarr)
                for phase in ('P', 'S'):
                    for arrival in arrivals[phase]:
                        arid = tbl_arrival.nextid("arid")
                        tbl_assoc.record = tbl_assoc.addnull()
                        tbl_arrival.record = tbl_arrival.addnull()
                        #print "updating arrival:", arrival.station, phase, arrival.time,  arid
                        scale = 0.5 if phase == 'P' else 1.0
                        noise = np.random.normal(scale=scale)
                        arrtime = arrival.time + noise
                        tbl_assoc.putv(("arid", arid),
                                       ("orid", orid),
                                       ("phase", phase),
                                       ("sta", arrival.station))
                        tbl_arrival.putv(("arid", arid),
                                         ("iphase", phase),
                                         ("sta", arrival.station),
                                         ("time", float(arrtime)))

if __name__ == "__main__":
    cfg = parse_config(sys.argv[1])
    main(cfg)
