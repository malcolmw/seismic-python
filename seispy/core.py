class Arrival(object):
    def __init__(self, sta, time, phase, arid=-1):
        self.sta = sta
        self.time = time
        self.phase = phase
        self.arid = arid

class Origin(object):
    def __init__(self, lat, lon, depth, time,
                 arrivals=(),
                 orid=-1,
                 evid=-1,
                 sdobs=-1):
        self.lat = lat
        self.lon = lon % 360.
        self.depth = depth
        self.time = time
        self.arrivals = ()
        self.add_arrivals(arrivals)
        self.orid = orid
        self.evid = evid
        self.sdobs = sdobs

    def __str__(self):
        return "origin: %.4f %.4f %.4f %.4f %.2f" % (self.lat,
                                                     self.lon,
                                                     self.depth,
                                                     self.time,
                                                     self.sdobs)

    def add_arrivals(self, arrivals):
        for arrival in arrivals:
            if not isinstance(arrival, Arrival):
                raise TypeError("not an Arrival object")
            self.arrivals += (arrival,)
        self.nass = len(self.arrivals)
        self.ndef = len(self.arrivals)

    def clear_arrivals(self):
        self.arrivals = ()


class Station(object):
    def __init__(self, name, lon, lat, elev):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.elev = elev
