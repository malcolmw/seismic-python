#!/usr/bin/env python

from ConfigParser import RawConfigParser
import os.path
import shutil
import struct
import subprocess
import sys
import tempfile
import numpy as np
from seispy.core import Origin, Station
from seispy.geometry import EARTH_RADIUS
from seispy.util import MultiThreadProcess
from seispy.velocity import VelocityModel

def parse_config(config_file):
    cfg, propgrid = {}, {}
    cfg_file = RawConfigParser()
    cfg_file.read(config_file)
    propgrid['h0'] = cfg_file.getfloat('General', 'h0')
    propgrid['lon0'] = cfg_file.getfloat('General', 'lon0')
    propgrid['lat0'] = cfg_file.getfloat('General', 'lat0')
    propgrid['dr'] = cfg_file.getfloat('General', 'dr')
    propgrid['dlon'] = cfg_file.getfloat('General', 'dlon')
    propgrid['dlat'] = cfg_file.getfloat('General', 'dlat')
    propgrid['nr'] = cfg_file.getint('General', 'nr')
    propgrid['nlon'] = cfg_file.getint('General', 'nlon')
    propgrid['nlat'] = cfg_file.getint('General', 'nlat')
    cfg['propgrid'] = propgrid
    cfg['velocity_model'] = cfg_file.get('General', 'velocity_model')
    cfg['topography'] = cfg_file.get('General', 'topography')
    cfg['stations'] = cfg_file.get('General', 'stations')
    cfg['sources'] = cfg_file.get('General', 'sources')
    cfg['n_sources'] = cfg_file.getint('General', 'n_sources')
    cfg['n_threads'] = cfg_file.getint('General', 'n_threads')
    return cfg

def generate_sources(cfg):
    n_sources = cfg['n_sources']
    grid = cfg['propgrid']
    lon0, lat0, h0 = grid['lon0'] % 360., grid['lat0'], grid['h0']
    nlon, nlat, nr = grid['nlon'], grid['nlat'], grid['nr']
    dlon, dlat, dr = grid['dlon'], grid['dlat'], grid['dr']
    lon_max = lon0 + (nlon - 1) * dlon
    lat_max = lat0 + (nlat - 1) * dlat
    r_max = EARTH_RADIUS + h0
    r0 = r_max - (nr - 1) * dr
    delta_lon = lon_max - lon0
    delta_lat = lat_max - lat0
    delta_r = r_max - r0
    lon = np.random.rand(n_sources) * delta_lon + lon0
    lat = np.random.rand(n_sources) * delta_lat + lat0
    z = EARTH_RADIUS - (np.random.rand(n_sources) * delta_r + r0)
    sources = []
    outfile = open("sources.dat", "w")
    for i in range(n_sources):
        sources += [Origin(lat[i], lon[i], z[i], 597628800., orid=i, evid=i)]
        outfile.write("%.4f %.4f %.4f %.3f\n" % (lat[i], lon[i], z[i], 597628800.))
    outfile.close()
    return sources

def write_frechet():
    ofile = open('frechet.in', 'w')
    ofile.write("0")
    ofile.close()

def write_gridsave():
    ofile = open('gridsave.in', 'w')
    ofile.write("1 1\n")
    ofile.write("1\n")
    ofile.write("1\n")
    ofile.close()

def write_mode_set():
    ofile = open('mode_set.in', 'w')
    ofile.write("F file_mode\n")
    ofile.write("T no_pp_mode\n")
    ofile.write("F parallel_mode\n")
    ofile.write("F display_mode\n")
    ofile.write("T save_rays_mode\n")
    ofile.write("F save_timefields_mode\n")
    ofile.close()

def write_source(lon, lat, depth):
    ofile = open('sources.in', 'w')
    ofile.write("1\n")
    ofile.write("0\n")
    ofile.write("%.4f %.4f %.4f\n" % (depth, lat, lon % 360.))
    ofile.write("1\n")
    ofile.write("1\n")
    ofile.write("0 2\n")
    ofile.write("1\n")
    ofile.close()

def write_receiver(cfg):
    ifile = open(cfg['stations'])
    stations = []
    for line in ifile:
        name, lon, lat, elev = line.split()
        lon, lat, elev = float(lon), float(lat), float(elev)
        stations += [Station(name, lon, lat, elev)]
    ifile.close()
    ofile = open('receivers.in', 'w')
    ofile.write("%d\n" % len(stations))
    for station in stations:
        rxlat0, rxlon0, elev = station.lat, station.lon, station.elev
        ofile.write("%.4f %.4f %.4f\n" % (-elev, rxlat0, rxlon0 % 360.))
        ofile.write("1\n")
        ofile.write("1\n")
        ofile.write("1\n")
    ofile.close()

def main():
    cfg = parse_config(os.path.abspath(sys.argv[1]))
    #print "loading velocity model"
    #vm = VelocityModel(cfg['velocity_model'],
    #                   cfg['topography'])
    #print "writing vgrids.in, interfaces.in and propgrid.in"
    #vm.write_fm3d(cfg['propgrid'])
    propgrid = cfg['propgrid']
    write_frechet()
    write_gridsave()
    write_mode_set()
    write_receiver(cfg)
    sources = generate_sources(cfg)
    os.mkdir("arrivals")
    os.mkdir("rays")
    config_params = {'n_threads': cfg['n_threads']}
    extra_args = {'input_init_args': (cfg,)}
    mtp = MultiThreadProcess(getter,
                             main_processor,
                             outputter,
                             config_params=config_params,
                             extra_args=extra_args)
    mtp.start()

def getter(cfg):
    for source in generate_sources(cfg):
        yield source

def main_processor(source):
    pwd = os.getcwd()
    workdir = tempfile.mkdtemp()
    os.chdir(workdir)
    lat0, lon0, z0 = source.lat, source.lon, source.depth
    write_source(lon0, lat0, z0)
    shutil.copyfile(os.path.join(pwd, "propgrid.in"), "propgrid.in")
    shutil.copyfile(os.path.join(pwd, "interfaces.in"), "interfaces.in")
    shutil.copyfile(os.path.join(pwd, "frechet.in"), "frechet.in")
    shutil.copyfile(os.path.join(pwd, "gridsave.in"), "gridsave.in")
    shutil.copyfile(os.path.join(pwd, "mode_set.in"), "mode_set.in")
    shutil.copyfile(os.path.join(pwd, "receivers.in"), "receivers.in")
    for phase in ('P', 'S'):
        shutil.copyfile(os.path.join(pwd, "vgrids.in_%s" % phase), "vgrids.in")
        subprocess.call("/home/shake/malcolcw/.local/bin/fm3d")
        shutil.move("arrivals.dat", os.path.join(pwd, "arrivals/%s%d.dat" % (phase, source.evid)))
        shutil.move("rays.dat", os.path.join(pwd, "rays/%s%d.dat" % (phase, source.evid)))
    os.chdir(pwd)
    return None

def outputter(obj):
    pass
    
if __name__ == "__main__":
    main()
