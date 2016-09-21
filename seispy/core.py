class Arrival(object):
    def __init__(self, sta, time, phase, arid=-1):
        self.sta = sta
        self.time = time
        self.phase = phase
        self.arid = arid

class Origin(object):
    def __init__(self, lat, lon, depth, time, arrivals=(), orid=-1, evid=-1):
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.time = time
        self.arrivals = ()
        self.add_arrivals(arrivals)
        self.orid = orid
        self.evid = evid

    def __str__(self):
        return "origin: %.4f %.4f %.4f %.4f" % (self.lat,\
                                                self.lon,\
                                                self.depth,\
                                                self.time)

    def add_arrivals(self, arrivals):
        for arrival in arrivals:
            if not isinstance(arrival, Arrival):
                raise TypeError("not an Arrival object")
            self.arrivals += (arrival,)

    def clear_arrivals(self):
        self.arrivals = ()


class Station(object):
    def __init__(self, name, lon, lat, elev):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.elev = elev
