from seispy import _ANTELOPE_DEFINED
from seispy.gather3c import Gather3C
from seispy.event import Arrival,\
                         Event,\
                         Magnitude,\
                         Origin
from seispy.network import Network,\
                           VirtualNetwork
from seispy.station import Channel,\
                           Station
from seispy.trace import Trace
if _ANTELOPE_DEFINED:
    from antelope.datascope import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from math import sqrt

if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")


class Database:
    def __init__(self, path, mode='r'):
        self.ptr = dbopen(path, mode)
        self.tables = {}
        for table in ("event",
                      "origin",
                      "assoc",
                      "arrival",
                      "site",
                      "sitechan",
                      "snetsta"):
            self.tables[table] = self.ptr.lookup(table=table)
        self.groups = {}
        view_assoc = self.tables["assoc"].join("arrival")
        _view = view_assoc.sort("orid")
        view_assoc.free()
        view_assoc = _view
        grp_assoc = view_assoc.group("orid")
        self.groups["assoc"] = (grp_assoc, view_assoc)

    def __getattr__(self, name):
        if name == "virtual_network":
            self.virtual_network = self.parse_virtual_network()
            return self.virtual_network
        else:
            raise AttributeError("no attribute %s" % name)

    def close(self):
        self.ptr.close()

    def get_gather3c(self, station, channel_set, starttime, endtime):
        traces = []
        for channel in channel_set:
            traces += [Trace(database_pointer=self.ptr,
                             station=station.name,
                             channel=channel.code,
                             starttime=starttime,
                             endtime=endtime)]
        return Gather3C(traces)

    def iterate_events(self,
                       subset=None,
                       parse_arrivals=True,
                       parse_magnitudes=True):
        tbl_event = self.tables["event"]
        view = tbl_event.join("origin")
        if subset:
            _view = view.subset(subset)
            view.free()
            view = _view
        event_view = view.separate("event")
        view.free()
        for event in event_view.iter_record():
            prefor = event.getv("prefor")[0]
            yield self.parse_origin(prefor,
                                    parse_arrivals=parse_arrivals,
                                    parse_magnitudes=parse_magnitudes)
        event_view.free()

    def iterate_origins(self,
                        subset=None,
                        parse_arrivals=True,
                        parse_magnitudes=True):
        tbl_origin = self.tables['origin']
        if subset:
            ptr = tbl_origin.subset(subset)
            is_view = True
        else:
            ptr = tbl_origin
            is_view = False
        for record in ptr.iter_record():
            orid = record.getv('orid')[0]
            yield self.parse_origin(orid,
                                    parse_arrivals=parse_arrivals,
                                    parse_magnitudes=parse_magnitudes)
        if is_view:
            ptr.free()

    def parse_event(self, evid, parse_arrivals=True, parse_magnitudes=True):
        tbl_event = self.tables["event"]

        view = tbl_event.subset("evid == %d" % evid)
        view.record = 0
        prefor = view.getv("prefor")[0]
        _view = view.join("origin")
        view.free()
        view = _view
        origins = ()
        for origin in view.iter_record():
            orid = origin.getv("orid")[0]
            origins += (self.parse_origin(orid,
                                          parse_arrivals=parse_arrivals,
                                          parse_magnitudes=parse_magnitudes), )
        event = Event(evid, origins=origins, prefor=prefor)
        view.free()
        return event

    def parse_origin(self, orid, parse_arrivals=True, parse_magnitudes=True):
        tbl_origin = self.tables["origin"]
        try:
            record = tbl_origin.find("orid == %d" % orid,
                                     first=tbl_origin.record)
        except DbfindEnd:
            try:
                record = tbl_origin.find("orid == %d" % orid,
                                         first=tbl_origin.record,
                                         reverse=True)
            except DbfindBeginning:
                raise IOError("orid doesn't exist")
        tbl_origin.record = record
        orid,\
            evid,\
            lat0,\
            lon0,\
            z0,\
            time0,\
            nass,\
            ndef,\
            author = tbl_origin.getv('orid',
                                     'evid',
                                     'lat',
                                     'lon',
                                     'depth',
                                     'time',
                                     'nass',
                                     'ndef',
                                     'auth')
        origin = Origin(lat0, lon0, z0, time0,
                        orid=orid,
                        evid=evid,
                        nass=nass,
                        ndef=ndef,
                        author=author)
        if parse_arrivals:
            self.groups["assoc"][0].record =\
                    self.groups["assoc"][0].find("orid == %d" % orid)
            arrivals = ()
            start, stop = self.groups["assoc"][0].get_range()
            for self.groups["assoc"][1].record in range(start, stop):
                record = self.groups["assoc"][1]
                arid, station, channel, time, phase = record.getv('arid',
                                                                  'sta',
                                                                  'chan',
                                                                  'time',
                                                                  'iphase')
                station = self.virtual_network.stations[station]
                arrivals += (Arrival(station,
                                     channel,
                                     time,
                                     phase,
                                     arid=arid),)
            origin.add_arrivals(arrivals)
        if parse_magnitudes:
            netmag_view = origin_view.join("netmag", outer=True)
            _view = netmag_view.separate("netmag")
            netmag_view.free()
            netmag_view = _view
            magnitudes = ()
            for netmag_row in netmag_view.iter_record():
                magid, mag, magtype = netmag_row.getv('magid',
                                                      'magnitude',
                                                      'magtype')
                magnitudes += (Magnitude(magtype, mag, magid=magid), )
            netmag_view.free()
            origin.add_magnitudes(magnitudes)
        return origin

    def parse_network(self, net_code):
        network = Network(net_code)
        tbl_snetsta = self.tables['snetsta']
        view = tbl_snetsta.subset("snet =~ /%s/" % net_code)
        _view = view.sort("sta", unique=True)
        view.free()
        view = _view
        for record in view.iter_record():
            code = record.getv('sta')[0]
            network.add_station(self.parse_station(code, net_code))
        view.free()
        return network

    def parse_station(self, name, net_code):
        tbl_sitechan = self.tables['sitechan']
        tbl_site = self.tables['site']
        sitechan_view = tbl_sitechan.subset("sta =~ /%s/" % name)
        site_view = tbl_site.join("snetsta")
        _site_view = site_view.subset("sta =~ /%s/ && snet =~ /%s/"
                                      % (name, net_code))
        site_view.free()
        site_view = _site_view
        site_view.record = 0
        lat, lon, elev, ondate, offdate = site_view.getv('lat',
                                                         'lon',
                                                         'elev',
                                                         'ondate',
                                                         'offdate')
        station = Station(name,
                          lon,
                          lat,
                          elev,
                          net_code,
                          ondate=ondate,
                          offdate=offdate)
        for record in sitechan_view.iter_record():
            code, ondate, offdate = record.getv('chan', 'ondate', 'offdate')
            if not code[1] == 'H' and not code[1] == 'N':
                continue
            channel = Channel(code, ondate, offdate)
            station.add_channel(channel)
        return station

    def parse_virtual_network(self):
        virtual_network = VirtualNetwork("ZZ")
        tbl_snetsta = self.tables['snetsta']
        view = tbl_snetsta.sort("snet", unique=True)
        for record in view.iter_record():
            net_code = record.getv("snet")[0]
            virtual_network.add_subnet(self.parse_network(net_code))
        view.free()
        return virtual_network

    def plot_origin(self, origin, topography=None, **kwargs):
        default_kwargs = {"resolution": 'c'}
        _kwargs = {}
        for kw in default_kwargs:
            if kw in kwargs:
                _kwargs[kw] = kwargs[kw]
            else:
                _kwargs[kw] = default_kwargs[kw]
        kwargs = _kwargs
        lat0, lon0, z0, t0 = origin.lat, origin.lon, origin.depth, origin.time
        X = [arrival.station.lon for arrival in origin.arrivals]
        Y = [arrival.station.lat for arrival in origin.arrivals]
        xmin, xmax = min([lon0] + X), max([lon0] + X)
        ymin, ymax = min([lat0] + Y), max([lat0] + Y)
        x0 = (xmax + xmin) / 2
        y0 = (ymax + ymin) / 2
        extent = max([sqrt((X[i] - x0) ** 2
                           + (Y[i] - y0) ** 2)\
                      for i in range(len(X))]) * 1.1
        extent = max(0.85, extent)
        m = Basemap(llcrnrlon=x0 - extent,
                    llcrnrlat=y0 - extent,
                    urcrnrlon=x0 + extent,
                    urcrnrlat=y0 + extent,
                    **kwargs)
#        if isinstance(topography, Surface):
#            surface = topography
#            m.pcolormesh(surface.XX,
#                         surface.YY,
#                         surface.ZZ, cmap=mpl.cm.terrain)
#            tX = np.linspace(x0 - extent, x0  + extent, 200)
#            tY = np.linspace(y0 - extent, y0 + extent, 200)
#            tXX, tYY = np.meshgrid(tX, tY, indexing='ij')
#            tZZ = np.empty(shape=tXX.shape)
#            for i in range(tXX.shape[0]):
#                for j in range(tXX.shape[1]):
#                    tZZ[i, j] = geoid(tXX[i, j] - 360., tYY[i, j])
#            m.pcolormesh(tXX, tYY, tZZ, cmap=mpl.cm.terrain)
#        else:
        m.arcgisimage(server='http://server.arcgisonline.com/arcgis',
                      service='USA_Topo_Maps')
        m.drawmapboundary()
        m.scatter(lon0, lat0, marker="*", color="r", s=100)
        m.scatter(X, Y, marker="v", color="g", s=50)
        plt.show()

    def write_origin(self, origin):
        tbl_origin = self.tables['origin']
        tbl_assoc = self.tables['assoc']
        orid = tbl_origin.nextid('orid')
        tbl_origin.record = tbl_origin.addnull()
        tbl_origin.putv(('orid', orid),
                        ('evid', origin.evid),
                        ('lat', origin.lat),
                        ('lon', origin.lon),
                        ('depth', origin.depth),
                        ('time', float(origin.time)),
                        ('auth', origin.author),
                        ('nass', len(origin.arrivals)),
                        ('ndef', len(origin.arrivals)))
        for arrival in origin.arrivals:
            tbl_assoc.record = tbl_assoc.addnull()
            tbl_assoc.putv(('orid', orid),
                           ('arid', arrival.arid),
                           ('sta', arrival.station),
                           ('phase', arrival.phase))
