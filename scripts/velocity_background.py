#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 22:15:38 2016

@author: malcolcw
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

from gazelle.datascope import Database
from seispy.velocity import VelocityModel

resolution = 'i'
marker_size = 100
parallel_mark_stride = 0.5
meridian_mark_stride = 0.5
label_positions = [1, 0, 0, 1]  #[L, R, T, B]
latmin = 32.38
latmax = 34.55
lonmin = 241.83
lonmax = 244.6


def main():
    origins = get_origins()
    for depth in range(1, 25):
        plot_map(origins, depth)


def get_origins():
    origins = []
    for year in range(1998, 2016):
        if year == 2010:
            continue
        db = Database("/home/shake/malcolcw/products/catalog/SJFZ/%d/SJFZ_%d"
                      % (year, year))
        for origin in db.iterate_origins(subset="depth > 25. && auth =~ "
                                         "/malcolcw:reloc/",
                                         parse_arrivals=False,
                                         parse_magnitudes=False):
            origins += [origin]
            print origin
        db.close()
    return origins


def plot_map(origins, depth):
    model = "/home/shake/malcolcw/products/velocity/FANG2016/original/VpVs.dat"
    topo = "/home/shake/malcolcw/data/mapping/ANZA/anza.xyz"
    vm = VelocityModel(model, topo)
    plt.figure(figsize=(12, 12))
    m = Basemap(llcrnrlon=lonmin,
                llcrnrlat=latmin,
                urcrnrlon=lonmax,
                urcrnrlat=latmax,
                resolution=resolution)
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawparallels(np.arange(latmin - latmin % parallel_mark_stride,
                              latmax - latmax % parallel_mark_stride +
                              parallel_mark_stride,
                              parallel_mark_stride),
                    labels=label_positions)
    m.drawmeridians(np.arange(lonmin - lonmin % meridian_mark_stride,
                              lonmax - lonmax % meridian_mark_stride +
                              meridian_mark_stride,
                              meridian_mark_stride),
                    labels=label_positions)
    X = np.linspace(lonmin, lonmax, 200)
    Y = np.linspace(latmin, latmax, 200)
    XX, YY = np.meshgrid(X, Y, indexing='ij')
    VV = np.empty(shape=XX.shape)
    for i in range(XX.shape[0]):
        for j in range(XX.shape[1]):
            VV[i, j] = vm.get_Vp(YY[i, j], XX[i, j], depth)
    m.pcolormesh(XX, YY, VV, cmap=mpl.cm.jet_r)
    m.colorbar()
    plt.scatter([o.lon for o in origins],
                [o.lat for o in origins],
                marker='.',
                s=10)
    plt.savefig("/home/shake/malcolcw/Desktop/depth_%d.png" % depth,
                format="png")
    plt.close()

if __name__ == "__main__":
    main()
