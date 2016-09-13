from math import degrees,\
                 pi,\
                 radians
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from geometry import EARTH_RADIUS

class Geoid(np.ndarray):
    def __new__(cls, infile):
        infile = open(infile)
        lons, lats, elevs = [], [], []
        for line in infile:
            lon, lat, elev = [float(v) for v in line.split()]
            lon = lon + 360 if lon < -180 else lon - 360 if lon > 360 else lon
            lons += [lon]
            lats += [lat]
            elevs += [elev]
        nlon = len(set(lons))
        nlat = len(set(lats))
        me = np.ndarray.__new__(cls, shape=(nlon, nlat))
        for i in range(nlon):
            for j in range(nlat):
                me[i, j] = elevs[i * nlat + j] / 1000. + EARTH_RADIUS
        me.coords = Coordinates(lons, lats)
        me._coords = Coordinates([radians(lon) for lon in lons],
                                [pi / 2 - radians(lat) for lat in lats])
        me.interpolate = LinearNDInterpolator(zip(me._coords.X1[0,:],
                                                     me._coords.X2[:,0]),
                                                 np.concatenate(me))
        me.lat_min, me.lat_max = min(lats), max(lats)
        me.lon_min, me.lon_max = min(lons), max(lons)
        me.phi_min, me.phi_max = min(me._coords.X1[0,:]), max(me._coords.X1[0,:])
        me.theta_min, me.theta_max = min(me._coords.X2[:,0]), max(me._coords.X2[:,0])
        return me

    def call(self, *args, **kwargs):
        return self._eval(*args, **kwargs)

    def _eval(self, u, v, coords="geographical"):
        if coords == "geographical":
            u = radians(u)
            v = radians(90. - v)
        return self.interpolate((u, v))
            

    def plot(self, lat=-999, lon=-999, npts=50):
        x, y = [], []
        if lat == -999:
            for lat in np.linspace(self.lat_min, self.lat_max, npts):
                x += [lat]
                y += [self.call(lon, lat)]
        elif lon == -999:
            for lon in np.linspace(self.lon_min, self.lon_max, npts):
                x += [lon]
                y += [self.call(lon, lat)]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y)
        plt.show()

class Coordinates(object):
    def __init__(self, x1, x2, system="geographical"):
        self.X1, self.X2 = np.meshgrid(x1, x2)
        self.system = system
