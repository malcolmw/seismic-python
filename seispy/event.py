# -*- coding: utf-8 -*-
from math import sqrt, pi
from seispy.util import validate_time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from obspy.geodetics import gps2dist_azimuth

from matplotlib.patches import Circle


class Arrival(object):
    """
    This is a container object to store data pertaining to phase arrivals.
    """
    def __init__(self,
                 station,
                 channel,
                 time,
                 phase,
                 arid=-1,
                 timeres=-999.000):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.phase = phase
        self.arid = arid
        self.timeres = timeres

    def __str__(self):
        return "%s:%s %s %s" % (self.station.name,
                                self.channel.code,
                                self.phase,
                                str(self.time))


class Detection(object):
    """
    This is a container object to store data pertaining to signal detections.
    """
    def __init__(self, station, channel, time, label):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.label = label


class Event(object):
    def __init__(self, evid, prefor=-1, origins=None):
        self.evid = evid
        self.prefor = prefor
        self.origins = ()
        if origins:
            self.add_origins(origins)

    def get_prefor(self):
        for origin in self.origins:
            if origin.orid == self.prefor:
                return origin
        raise ValueError("invalid prefor")

    def add_origins(self, origins):
        for origin in origins:
            if not isinstance(origin, Origin):
                raise TypeError("not an Origin object")
            self.origins += (origin, )


class Magnitude(object):
    def __init__(self, magtype, magnitude, magid=-1):
        self.magtype = magtype
        self.value = magnitude
        self.magid = magid

    def __str__(self):
        return "%s: %.2f" % (self.magtype, self.value)


class Origin(object):
    def __init__(self, lat, lon, depth, time,
                 arrivals=None,
                 magnitudes=None,
                 orid=-1,
                 evid=-1,
                 sdobs=-1,
                 nass=-1,
                 ndef=-1,
                 author=None):
        self.lat = lat
        self.lon = lon % 360.
        self.depth = depth
        self.time = validate_time(time)
        self.arrivals = ()
        self.magnitudes = ()
        self.stations = {}
        if arrivals:
            self.add_arrivals(arrivals)
        if magnitudes:
            self.add_magnitudes(magnitudes)
        self.orid = orid
        self.evid = evid
        self.sdobs = sdobs
        self.nass = nass
        self.ndef = ndef
        self.author = author

    def __getattr__(self, attr):
        if attr == "quality":
            return self._quality()
        else:
            raise AttributeError

    def __str__(self):
        return "origin: %d %.4f %.4f %.4f %s %s" % (self.orid,
                                                    self.lat,
                                                    self.lon,
                                                    self.depth,
                                                    self.time,
                                                    self.author)

    def _quality(self):
        if self.is_in_neighbourhood_A():
            return "A"
        elif self.is_in_neighbourhood_B() and\
                self.azimuthal_distribution_coefficient() > 1 / 3.:
            return "B"
        else:
            return "C"

    def add_arrivals(self, arrivals):
        for arrival in arrivals:
            if not isinstance(arrival, Arrival):
                raise TypeError("not an Arrival object")
            self.arrivals += (arrival, )
            if arrival.station.name not in self.stations:
                self.stations[arrival.station.name] = arrival.station
        self.nass = len(self.arrivals)
        self.ndef = len(self.arrivals)

    def add_magnitudes(self, magnitudes):
        for magnitude in magnitudes:
            if not isinstance(magnitude, Magnitude):
                raise TypeError("not an Arrival object")
            self.magnitudes += (magnitude, )

    def get_magnitude(self, magtype=None):
        """
        This should return the preferred magnitude based on some order
        of precedence OR the magnitude of the type provided by the magtype
        keyword, if it exists.
        """
        return None if len(self.magnitudes) == 0 else self.magnitudes[0]

    def is_in_neighbourhood_A(self):
        coordinates = np.asarray([[self.stations[key].lon,
                                   self.stations[key].lat]
                                  for key in self.stations])
        centroid = coordinates.mean(axis=0)
        median_dist = np.median(np.asarray([sqrt((centroid[0] -
                                                  self.stations[key].lon) ** 2 +
                                                 (centroid[1] -
                                                  self.stations[key].lat) ** 2)
                                            for key in self.stations]))
        density = len(self.stations) / (pi * median_dist ** 2)
        # radius of Quality A neighbourhood
        RA = 0.01 * median_dist * density
        for key in self.stations:
            distance = sqrt((centroid[0] - self.lon) ** 2 +
                            (centroid[1] - self.lat) ** 2)
            if distance < RA:
                return True
        return False

    def is_in_neighbourhood_B(self):
        coordinates = np.asarray([[self.stations[key].lon,
                                   self.stations[key].lat] for key in self.stations])
        centroid = coordinates.mean(axis=0)
        median_dist = np.median(np.asarray([sqrt((centroid[0] -
                                                  self.stations[key].lon) ** 2 +
                                                 (centroid[1] -
                                                  self.stations[key].lat) ** 2)
                                            for key in self.stations]))
        for key in self.stations:
            distance = sqrt((self.stations[key].lat - self.lat) ** 2 +
                            (self.stations[key].lon - self.lon) ** 2)
            if distance < median_dist:
                return True

    def azimuthal_distribution_coefficient(self):
        azimuths = []
        for arrival in self.arrivals:
            d, abaz, baaz = gps2dist_azimuth(self.lat,
                                             self.lon,
                                             arrival.station.lat,
                                             arrival.station.lon)
            if abaz not in azimuths:
                azimuths += [abaz]
        hist = np.histogram(azimuths,
                            bins=18,
                            range=(0., 360.))
        return sum([1 for count in hist[0] if count > 0]) /\
               float(len(hist[1]) - 1)

    def clear_arrivals(self):
        self.arrivals = ()
        self.stations = {}

    def clear_magnitudes(self):
        self.magnitudes = ()

    def plot(self,
             cmap=None,
             label_positions=[1, 0, 1, 0],
             meridian_mark_stride=0.5,
             parallel_mark_stride=0.5,
             resolution='c',
             save=False,
             show=True,
             subplot_ax=None):
        lat0, lon0 = self.lat, self.lon
        X = [arrival.station.lon for arrival in self.arrivals]
        Y = [arrival.station.lat for arrival in self.arrivals]
        if cmap is not None:
            colors = [cmap(gps2dist_azimuth(lat0, lon0, Y[i], X[i])[1] / 360.)
                      for i in range(len(X))]
        else:
            colors = ["g" for i in range(len(X))]
        xmin, xmax = min([lon0] + X), max([lon0] + X)
        ymin, ymax = min([lat0] + Y), max([lat0] + Y)
        x0 = (xmax + xmin) / 2
        y0 = (ymax + ymin) / 2
        extent = max([sqrt((X[i] - x0) ** 2 + (Y[i] - y0) ** 2)
                      for i in range(len(X))]) * 1.1
        extent = max(0.85, extent)
        if subplot_ax:
            ax = subplot_ax
        else:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        m = Basemap(llcrnrlon=x0 - extent,
                    llcrnrlat=y0 - extent,
                    urcrnrlon=x0 + extent,
                    urcrnrlat=y0 + extent,
                    resolution=resolution)
        m.arcgisimage(server='http://server.arcgisonline.com/arcgis',
                      service='USA_Topo_Maps')
        m.drawmapboundary()
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        if ymax - ymin < 1.0:
            parallel_mark_stride = 0.2
        elif 1.0 <= ymax - ymin < 2.5:
            parallel_mark_stride = 0.5
        else:
            parallel_mark_stride = 1.0
        if xmax - xmin < 1.0:
            meridian_mark_stride = 0.2
        elif 1.0 <= xmax - xmin < 2.5:
            meridian_mark_stride = 0.5
        else:
            meridian_mark_stride = 1.0
        m.drawparallels(np.arange(ymin - ymin % parallel_mark_stride,
                        ymax - ymax % parallel_mark_stride +
                        parallel_mark_stride,
                        parallel_mark_stride),
                        labels=label_positions)
        m.drawmeridians(np.arange(xmin - xmin % meridian_mark_stride,
                        xmax - xmax % meridian_mark_stride +
                        meridian_mark_stride,
                        meridian_mark_stride),
                        labels=label_positions)
        m.scatter(lon0, lat0, marker="*", color="r", s=100)
        [m.scatter(X[i], Y[i], marker="v", color=colors[i], s=50)
            for i in range(len(X))]
        bbox_props = {"boxstyle": "round", "facecolor": "white", "alpha": 0.5}
        plt.figtext(0.95, 0.90,
                    "{:>7s}: {:>6s}\n"\
                    "{:>7s}: {:>6.2f}\n"\
                    "{:>7s}: {:>6.2f}\n"\
                    "{:>7s}: {:>6.2f}\n"\
                    "{:>7s}: {:>6d}".format("quality",
                                          self.quality,
                                          "lat",
                                          self.lat,
                                          "lon",
                                          self.lon,
                                          "depth",
                                          self.depth,
                                          "orid",
                                          self.orid),
                    bbox=bbox_props,
                    horizontalalignment="right",
                    verticalalignment="top",
                    family="monospace")
        plt.subplots_adjust(right=0.75)
        if subplot_ax:
            return ax
        if save:
            plt.savefig(save + ".png", format="png")
        if show:
            plt.show()
            
    def plot_special(self,
             cmap=None,
             label_positions=[1, 0, 1, 0],
             meridian_mark_stride=0.5,
             parallel_mark_stride=0.5,
             resolution='c',
             show=True,
             subplot_ax=None):
        lat0, lon0 = self.lat, self.lon
        X = [arrival.station.lon for arrival in self.arrivals]
        Y = [arrival.station.lat for arrival in self.arrivals]
        if cmap is not None:
            colors = [cmap(gps2dist_azimuth(lat0, lon0, Y[i], X[i])[1] / 360.)
                      for i in range(len(X))]
        else:
            colors = ["g" for i in range(len(X))]
        xmin, xmax = min([lon0] + X), max([lon0] + X)
        ymin, ymax = min([lat0] + Y), max([lat0] + Y)
        x0 = (xmax + xmin) / 2
        y0 = (ymax + ymin) / 2
        extent = max([sqrt((X[i] - x0) ** 2 + (Y[i] - y0) ** 2)
                      for i in range(len(X))]) * 1.1
        extent = max(0.85, extent)
        if subplot_ax:
            ax = subplot_ax
        else:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        m = Basemap(llcrnrlon=x0 - extent,
                    llcrnrlat=y0 - extent,
                    urcrnrlon=x0 + extent,
                    urcrnrlat=y0 + extent,
                    resolution=resolution)
        m.arcgisimage(server='http://server.arcgisonline.com/arcgis',
                      service='USA_Topo_Maps')
        m.drawmapboundary()
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        if ymax - ymin < 1.0:
            parallel_mark_stride = 0.2
        elif 1.0 <= ymax - ymin < 2.5:
            parallel_mark_stride = 0.5
        else:
            parallel_mark_stride = 1.0
        if xmax - xmin < 1.0:
            meridian_mark_stride = 0.2
        elif 1.0 <= xmax - xmin < 2.5:
            meridian_mark_stride = 0.5
        else:
            meridian_mark_stride = 1.0
        m.drawparallels(np.arange(ymin - ymin % parallel_mark_stride,
                        ymax - ymax % parallel_mark_stride +
                        parallel_mark_stride,
                        parallel_mark_stride),
                        labels=label_positions)
        m.drawmeridians(np.arange(xmin - xmin % meridian_mark_stride,
                        xmax - xmax % meridian_mark_stride +
                        meridian_mark_stride,
                        meridian_mark_stride),
                        labels=label_positions)
        m.scatter(lon0, lat0, marker="*", color="r", s=100)
        [m.scatter(X[i], Y[i], marker="v", color=colors[i], s=50)
            for i in range(len(X))]
        stations = {}
        for arrival in self.arrivals:
            if arrival.station.name not in stations:
                stations[arrival.station.name] = arrival.station
        coordinates = np.asarray([[stations[key].lat,
                                   stations[key].lon] for key in stations])
        centroid = coordinates.mean(axis=0)
        median_dist = np.median(np.asarray([sqrt((centroid[0] - stations[key].lat) ** 2 +
                                     (centroid[1] - stations[key].lon) ** 2)
                                for key in stations]))
        ax = plt.gca()
        [ax.add_patch(Circle((X[i], Y[i]),
                             median_dist,
                             fill=False)) for i in range(len(X))]
        density = len([key for key in stations]) / (pi * median_dist ** 2)
        ax.add_patch(Circle((centroid[1], centroid[0]),
                            median_dist * (density / 100.),
                            alpha=0.25))
        if subplot_ax:
            return ax
        elif show:
            plt.show()
