from seispy import _ANTELOPE_DEFINED
if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")

from antelope.datascope import *

from seispy.core import Gather3C,\
                        Trace

class Database:
    def __init__(self, path, mode='r'):
        self.ptr = dbopen(path, mode)

    def close(self):
        self.ptr.close()

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
