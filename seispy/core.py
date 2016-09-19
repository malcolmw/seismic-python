class Arrival(object):
    def __init__(self, sta, time, phase, deltime):
        self.sta = sta
        self.time = time
        self.phase = phase
        self.deltime = deltime

class Origin(object):
    def __init__(self, lat, lon, depth, time, arrivals=()):
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.time = time
        self.arrivals = ()
        self.add_arrivals(arrivals)

    def add_arrivals(self, arrivals):
        for arrival in arrivals:
            if not isinstance(arrival, Arrival):
                raise TypeError("not an Arrival object")
            self.arrivals += (arrival,)

class Station(object):
    def __init__(self, name, lon, lat, elev):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.elev = elev
