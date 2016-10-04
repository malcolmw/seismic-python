from seispy import _ANTELOPE_DEFINED
if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")

from antelope.datascope import *

from seispy.core import Arrival,\
                        Gather3C,\
                        Origin,\
                        Trace

class Database:
    def __init__(self, path, mode='r'):
        self.ptr = dbopen(path, mode)

    def close(self):
        self.ptr.close()

    def iterate_events(self, subset=None):
        tbl_event = self.ptr.lookup(table="event")
        ptr = tbl_event.join("origin")
        _ptr = ptr.subset("orid == prefor")
        ptr.free()
        ptr = _ptr
        if subset:
            _ptr = ptr.subset(subset)
            ptr.free()
            ptr = _ptr
        for event in ptr.iter_record():
            orid, evid, lat0, lon0, z0, time0 = event.getv('orid',
                                                              'evid',
                                                              'lat',
                                                              'lon',
                                                              'depth',
                                                              'time')
            view_origin = ptr.subset("orid == %d" % orid)
            _view = view_origin.join('assoc', outer=True)
            view_assoc = _view.separate('assoc')
            _view.free()
            view_origin.free()
            _view = view_assoc.join('arrival')
            view_assoc.free()
            view_assoc = _view
            arrivals = ()
            for record in view_assoc.iter_record():
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
            view_assoc.free()
            yield origin
        ptr.free()

    def iterate_origins(self, subset=None):
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
            view_origin = ptr.subset("orid == %d" % orid)
            _view = view_origin.join('assoc', outer=True)
            view_assoc = _view.separate('assoc')
            _view.free()
            view_origin.free()
            _view = view_assoc.join('arrival')
            view_assoc.free()
            view_assoc = _view
            arrivals = ()
            for record in view_assoc.iter_record():
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
            view_assoc.free()
            yield origin
        if is_view:
            ptr.free()

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
        view_sitechan = tbl_sitechan.subset("sta =~ /%s/" % code)
        view_site = tbl_site.subset("sta =~ /%s/" % code)
        view_site.record = 0
        lat, lon, elev, ondate, offdate = view_site.getv('lat',
                                                         'lon',
                                                         'elev',
                                                         'ondate',
                                                         'offdate')
        station = Station(code, lon, lat, elev, ondate=ondate, offdate=offdate)
        for record in view_sitechan.iter_record():
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
