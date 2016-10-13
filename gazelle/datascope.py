from seispy import _ANTELOPE_DEFINED

if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")
class Database:
    def __init__(self, path, mode='r'):
        self.ptr = dbopen(path, mode)

    def close(self):
        self.ptr.close()

    def iterate_events(self, subset=None, parse_arrivals=True, parse_magnitudes=True):
        tbl_event = self.ptr.lookup(table="event")
        view = tbl_event.join("origin")
        if subset:
            _view = view.subset(subset)
            view.free()
            view = _view
        event_view = view.separate("event")
        view.free()
        for event in event_view.iter_record():
            evid = event.getv("evid")[0]
            yield self.parse_event(evid,
                                   parse_arrivals=parse_arrivals,
                                   parse_magnitudes=parse_magnitudes)
        event_view.free()


    def iterate_origins(self, subset=None, parse_arrivals=True, parse_magnitudes=True):
        tbl_origin = self.ptr.lookup(table='origin')
        if subset:
            ptr = tbl_origin.subset(subset)
            is_view = True
        else:
            ptr = tbl_origin
            is_view = False
        for origin_row in ptr.iter_record():
            orid, evid, lat0, lon0, z0, time0 = origin_row.getv('orid',
                                                              'evid',
                                                              'lat',
                                                              'lon',
                                                              'depth',
                                                              'time')
            origin_view = ptr.subset("orid == %d" % orid)
            _view = origin_view.join('assoc', outer=True)
            assoc_view = _view.separate('assoc')
            _view.free()
            origin_view.free()
            _view = assoc_view.join('arrival')
            assoc_view.free()
            assoc_view = _view
            arrivals = ()
            for record in assoc_view.iter_record():
                arid, station, channel, time, phase = record.getv('arid',
                                                                  'sta',
                                                                  'chan',
                                                                  'time',
                                                                  'iphase')
                arrivals += (Arrival(station, channel, time, phase, arid=arid),)
            origin = Origin(lat0, lon0, z0, time0,
                            arrivals=arrivals,
                            orid=orid,
                            evid=evid)
            assoc_view.free()
            yield origin
        if is_view:
            ptr.free()

    def parse_event(self, evid, parse_arrivals=True, parse_magnitudes=True):
        tbl_event = self.ptr.lookup(table="event")
        view = tbl_event.subset("evid == %d" % evid)
        view.record = 0
        prefor = view.getv("prefor")[0]
        _view = view.join("origin")
        view.free()
        view = _view
        origins=()
        for origin in view.iter_record():
            orid = origin.getv("orid")[0]
            origins += (self.parse_origin(orid,
                                          parse_arrivals=parse_arrivals,
                                          parse_magnitudes=parse_magnitudes), )
        event = Event(evid, origins=origins, prefor=prefor)
        view.free()
        return event

    def parse_origin(self, orid, parse_arrivals=True, parse_magnitudes=True):
        tbl_origin = self.ptr.lookup(table="origin")
        origin_view = tbl_origin.subset("orid == %d" % orid)
        origin_view.record = 0
        orid, evid, lat0, lon0, z0, time0 = origin_view.getv('orid',
                                                             'evid',
                                                             'lat',
                                                             'lon',
                                                             'depth',
                                                             'time')
        origin = Origin(lat0, lon0, z0, time0,
                        orid=orid,
                        evid=evid)
        if parse_arrivals:
            _view = origin_view.join('assoc', outer=True)
            assoc_view = _view.separate('assoc')
            _view.free()
            _view = assoc_view.join('arrival')
            assoc_view.free()
            assoc_view = _view
            arrivals = ()
            for record in assoc_view.iter_record():
                arid, station, channel, time, phase = record.getv('arid',
                                                                  'sta',
                                                                  'chan',
                                                                  'time',
                                                                  'iphase')
                arrivals += (Arrival(station, channel, time, phase, arid=arid),)
            assoc_view.free()
            origin.add_arrivals(arrivals)
        if parse_magnitudes:
            netmag_view = origin_view.join("netmag", outer=True)
            _view = netmag_view.separate("netmag")
            netmag_view.free()
            netmag_view = _view
            magnitudes = ()
            for netmag_row in netmag_view.iter_record():
                magid, mag, magtype = netmag_row.getv('magid', 'magnitude', 'magtype')
                magnitudes += (Magnitude(magtype, mag, magid=magid), )
            netmag_view.free()
            origin.add_magnitudes(magnitudes)
        return origin
        

    def parse_network(self, net_code):
        from seispy.core import Network
        network = Network(net_code)
        tbl_snetsta = self.ptr.lookup(table='snetsta')
        view = tbl_snetsta.subset("snet =~ /%s/" % net_code)
        _view = view.sort("sta", unique=True)
        view.free()
        view = _view
        for record in view.iter_record():
            code = record.getv('sta')[0]
            network.add_station(self.parse_station(code))
        view.free()
        return network

    def parse_station(self, code):
        from seispy.core import Channel, Station
        tbl_sitechan = self.ptr.lookup(table='sitechan')
        tbl_site = self.ptr.lookup(table='site')
        sitechan_view = tbl_sitechan.subset("sta =~ /%s/" % code)
        site_view = tbl_site.subset("sta =~ /%s/" % code)
        site_view.record = 0
        lat, lon, elev, ondate, offdate = site_view.getv('lat',
                                                         'lon',
                                                         'elev',
                                                         'ondate',
                                                         'offdate')
        station = Station(code, lon, lat, elev, ondate=ondate, offdate=offdate)
        for record in sitechan_view.iter_record():
            code, ondate, offdate = record.getv('chan', 'ondate', 'offdate')
            if not code[1] == 'H' and not code[1] == 'N':
                continue
            channel = Channel(code, ondate, offdate)
            station.add_channel(channel)
        return station

    def parse_virtual_network(self, vnet_code):
        from seispy.core import VirtualNetwork
        virtual_network = VirtualNetwork(vnet_code)
        tbl_snetsta = self.ptr.lookup(table='snetsta')
        view = tbl_snetsta.sort("snet", unique=True)
        for record in view.iter_record():
            net_code = record.getv("snet")[0]
            virtual_network.add_subnet(self.parse_network(net_code))
        view.free()
        return virtual_network

    def get_gather3c(self, station, channel_set, starttime, endtime):
        from seispy.core import Trace
        traces = []
        for channel in channel_set:
            traces += [Trace(database_pointer=self.ptr,
                             station=station.name,
                             channel=channel.code,
                             starttime=starttime,
                             endtime=endtime)]
        return Gather3C(traces)

from antelope.datascope import *

from seispy.core import Arrival,\
                        Event,\
                        Gather3C,\
                        Magnitude,\
                        Origin,\
                        Trace

