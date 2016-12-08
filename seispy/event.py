# -*- coding: utf-8 -*-
from math import ceil,\
                 pi,\
                 sqrt
import seispy as sp
import seispy.burrow
from seispy.util import validate_time
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Bbox
from mpl_toolkits.basemap import Basemap
import numpy as np
from obspy.core import Stream
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
                 snr=-1,
                 timeres=-999.000):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.phase = phase
        self.arid = arid
        self.snr = snr
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
    def __init__(self, station, channel, time, label, snr=-1):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.label = label
        self.snr = snr


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
        return "origin: %d %.4f %.4f %.4f %s %s" % (self.evid,
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

    def get_magnitude(self, magtype=None):
        """
        This should return the preferred magnitude based on some order
        of precedence OR the magnitude of the type provided by the magtype
        keyword, if it exists.
        """
        return None if len(self.magnitudes) == 0 else self.magnitudes[0]
        
    def get_rms(self, ttgrid):
        r, theta, phi = sp.geometry.geo2sph(self.lat, self.lon, self.depth)
        tt = np.asarray([ttgrid.get_tt(arrival.station.name,
                                       arrival.phase,
                                       r,
                                       theta,
                                       phi) for arrival in self.arrivals])
        at = np.asarray([arrival.time.timestamp for arrival in self.arrivals])
        residuals = at - (self.time.timestamp + tt)
        return np.sqrt(np.mean(np.square(residuals)))

    def is_in_neighbourhood_A(self):
        stations = self.stations
        coordinates = np.asarray([[stations[key].lon,
                                   stations[key].lat]
                                  for key in stations])
        centroid = coordinates.mean(axis=0)
        median_dist = np.median(np.asarray([sqrt((centroid[0] -
                                                  stations[key].lon) ** 2 +
                                                 (centroid[1] -
                                                  stations[key].lat) ** 2)
                                            for key in stations]))
        density = len(stations) / (pi * median_dist ** 2)
        # radius of Quality A neighbourhood
        RA = 0.01 * median_dist * density
        for key in stations:
            distance = sqrt((centroid[0] - self.lon) ** 2 +
                            (centroid[1] - self.lat) ** 2)
            if distance < RA:
                return True
        return False

    def is_in_neighbourhood_B(self):
        stations = self.stations
        coordinates = np.asarray([[stations[key].lon,
                                   stations[key].lat] for key in stations])
        centroid = coordinates.mean(axis=0)
        median_dist = np.median(np.asarray([sqrt((centroid[0] -
                                                  stations[key].lon) ** 2 +
                                                 (centroid[1] -
                                                  stations[key].lat) ** 2)
                                            for key in stations]))
        for key in stations:
            distance = sqrt((stations[key].lat - self.lat) ** 2 +
                            (stations[key].lon - self.lon) ** 2)
            if distance < median_dist:
                return True

    def clear_arrivals(self):
        self.arrivals = ()
        self.stations = {}

    def clear_magnitudes(self):
        self.magnitudes = ()

    def plot(self,
             filter=None,
             save=False,
             show=True,
             ttgrid=None):
        st = Stream()
        willy = seispy.burrow.Groundhog()
        distance = sorted([gps2dist_azimuth(self.lat,
                                            self.lon,
                                            arrival.station.lat,
                                            arrival.station.lon)[0]
                           for arrival in self.arrivals])
        dmin, dmax = min(distance), max(distance)
        startlag = dmin / 6000. - 7
        endlag = dmax / 2000. + 5
        for arrival in self.arrivals:
            st += willy.fetch(arrival.station.name,
                              arrival.channel.code,
                              starttime=self.time + startlag,
                              endtime=self.time + endlag)
        arrivals = sorted(self.arrivals,
                          key=lambda arrival: (arrival.station.network,
                                               arrival.station.name,
                                               arrival.channel))
        if filter is not None:
            st.filter(*filter[0], **filter[1])
        st.trim(starttime=self.time + startlag + 2.)
        st.normalize()
        MAX_TRACES = 9
        ncol = int(ceil(len(st) / float(MAX_TRACES))) + 1
        nrow = int(ceil(len(st) / float(ncol - 1)))
        gs = GridSpec(nrow, ncol)
        gs.update(hspace=0, wspace=0)
        width = 1600
        height = width / float(ncol)
        print width, height
        fig = st.plot(size=(width, height),
                      handle=True)
        row, col = 0, 0
        for i in range(len(fig.axes)):
            ax = fig.axes[i]
            arrival = arrivals[i]
            color = "r" if arrival.phase == "P"\
                else "g" if arrival.phase == "S" else "b"
            ax.axvline(arrival.time.toordinal() +
                       arrival.time._get_hours_after_midnight() / 24.,
                       color=color,
                       linewidth=2,
                       alpha=0.75)
            if ttgrid is not None:
                r, theta, phi = sp.geometry.geo2sph(self.lat,
                                                    self.lon,
                                                    self.depth)
                predicted = self.time + ttgrid.get_tt(arrival.station.name,
                                                      arrival.phase,
                                                      r,
                                                      theta,
                                                      phi)
                ax.axvline(predicted.toordinal() +
                           predicted._get_hours_after_midnight() / 24.,
                           color=color,
                           linewidth=2,
                           linestyle="--",
                           alpha=0.75)
            if row % nrow == 0:
                col += 1
                row = 0
            position = gs[row, col].get_position(fig)
            ax.set_position(position)
            ax.get_yaxis().set_visible(False)
            row += 1
        for ax in fig.axes[nrow - 1::nrow] + [fig.axes[-1]]:
            ax.set_xticklabels(ax.get_xticklabels(),
                               visible=True,
                               fontsize=10,
                               rotation=-15,
                               horizontalalignment="left")
        gs.update(wspace=0.2)
        postl = gs[0].get_position(fig)
        posbl = gs[ncol * (nrow - 1)].get_position(fig)
        bbox_map = Bbox(((posbl.x0, posbl.y0), (posbl.x1, postl.y1)))
        ax = fig.add_axes(bbox_map)
        self.plot_map(ax=ax)
        fig.suptitle("%s  (ID #%d)" % (self.time, self.evid))
        if save:
            plt.savefig("%s.png" % save, format="png")
        if show:
            plt.show()
        else:
            plt.close()

    def plot_map(self,
                 ax=None):
        X = [arrival.station.lon for arrival in self.arrivals]
        Y = [arrival.station.lat for arrival in self.arrivals]
        extent = max([sqrt((X[i] - self.lon) ** 2 + (Y[i] - self.lat) ** 2)
                      for i in range(len(X))]) * 1.1
        extent = max(0.85, extent)
        m = Basemap(llcrnrlon=self.lon - extent,
                    llcrnrlat=self.lat - extent,
                    urcrnrlon=self.lon + extent,
                    urcrnrlat=self.lat + extent,
                    resolution='i',
                    ax=ax)
        if ax is None:
            ax = plt.gca()
        m.arcgisimage(server='http://server.arcgisonline.com/arcgis',
                      service='USA_Topo_Maps')
        m.drawmapboundary()
        # orient ticklabels
        m.drawmeridians(np.arange(-180.0, 180.0, 0.5),
                        labels=[1, 0, 0, 1],
                        fontsize=10,
                        rotation=15)
        m.drawparallels(np.arange(-90.0, 90.0, 0.5),
                        labels=[1, 0, 0, 1],
                        fontsize=10)
        m.plot(self.lon,
               self.lat,
               marker="*",
               markersize=15.,
               color=cm.hot(self.depth / 20.))
        stations = {}
        for arrival in self.arrivals:
            color = "r" if arrival.phase == "P" else "g"
            station = arrival.station
            if station.name not in stations:
                stations[station.name] = (station.lon,
                                          station.lat,
                                          color,
                                          "full")
            else:
                stations[station.name] = (station.lon,
                                          station.lat,
                                          "g",
                                          "right")
        for station in stations:
            m.plot(stations[station][0],
                   stations[station][1],
                   marker="v",
                   markersize=10,
                   color=stations[station][2],
                   fillstyle=stations[station][3],
                   markerfacecoloralt="r")
        bbox_props = {"boxstyle": "round", "facecolor": "white", "alpha": 0.5}
        x, y = m(self.lon - extent, self.lat + extent)
        ax = plt.gca()
        ax.text(x + 0.05 * extent, y - 0.05 * extent,
                "{:>7s}: {:>6s}\n"
                "{:>7s}: {:>6.2f}\n"
                "{:>7s}: {:>6.2f}\n"
                "{:>7s}: {:>6.2f}\n"
                "{:>7s}: {:>6d}".format("quality",
                                        self.quality,
                                        "lat",
                                        self.lat,
                                        "lon",
                                        self.lon - 360.,
                                        "depth",
                                        self.depth,
                                        "orid",
                                        self.orid),
                bbox=bbox_props,
                horizontalalignment="left",
                verticalalignment="top",
                family="monospace")


def test():
    import gazelle.datascope
#    database = gazelle.datascope.Database("/home/shake/malcolcw/projects/SJFZ/"
#                                          "dbs/2013-droptest/SJFZ_2013")
    database = gazelle.datascope.Database("/home/shake/malcolcw/data/"
                                          "ZR_catalog/anza_2013")
    for origin in database.iterate_events(parse_magnitudes=False):
        origin.plot(filter=(("highpass",), {"freq": 3.0}))

if __name__ == "__main__":
    test()