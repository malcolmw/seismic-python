# -*- coding: utf-8 -*-
from seispy.util import validate_time


class Arrival(object):
    """
    This is a container object to store data pertaining to phase arrivals.
    """
    def __init__(self, station, channel, time, phase, arid=-1):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.phase = phase
        self.arid = arid


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

    def __str__(self):
        return "origin: %.4f %.4f %.4f %s %s" % (self.lat,
                                                   self.lon,
                                                   self.depth,
                                                   self.time,
                                                   self.author)

    def add_arrivals(self, arrivals):
        for arrival in arrivals:
            if not isinstance(arrival, Arrival):
                raise TypeError("not an Arrival object")
            self.arrivals += (arrival, )
        self.nass = len(self.arrivals)
        self.ndef = len(self.arrivals)

    def add_magnitudes(self, magnitudes):
        for magnitude in magnitudes:
            if not isinstance(magnitude, Magnitude):
                raise TypeError("not an Arrival object")
            self.magnitudes += (magnitude, )

    def clear_arrivals(self):
        self.arrivals = ()

    def clear_magnitudes(self):
        self.magnitudes = ()
