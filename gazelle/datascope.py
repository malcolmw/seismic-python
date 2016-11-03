from seispy import _ANTELOPE_DEFINED
if _ANTELOPE_DEFINED:
    from antelope.datascope import *
if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")
from seispy.gather import Gather,\
                          Gather3C
from seispy.event import Arrival,\
                         Event,\
                         Magnitude,\
                         Origin
from seispy.network import Network,\
                           VirtualNetwork
from seispy.station import Channel,\
                           Station
from seispy.trace import Trace
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from math import sqrt


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
        
    def get_prefor(self, evid, **kwargs):
        tbl_event = self.tables["event"]
        tbl_event.record = tbl_event.find("evid == %d" % evid)
        prefor = tbl_event.getv("prefor")[0]
        return self.parse_origin(prefor, **kwargs)

    def load_trace(self, station, channel, starttime, endtime):
        trace = Trace(database_pointer=self.ptr,
                      station=station,
                      channel=channel,
                      starttime=starttime,
                      endtime=endtime)
        return trace
        
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
            ptr = tbl_origin.join('netmag', outer=True)
            _ptr = ptr.subset(subset)
            ptr.free()
            ptr = _ptr
            _ptr = ptr.separate('origin')
            ptr.free()
            ptr = _ptr
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
                try:
                    record = tbl_origin.find("orid == %d" % orid)
                except DbfindEnd:
                    raise IOError("orid %d doesn't exist" % orid)
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
                try:
                    channel = station.channels[channel]
                except KeyError:
                    channel = Channel(channel, -1, -1)
                arrivals += (Arrival(station,
                                     channel,
                                     time,
                                     phase,
                                     arid=arid),)
            origin.add_arrivals(arrivals)
        if parse_magnitudes:
            netmag_view = tbl_origin.join("netmag", outer=True)
            _view = netmag_view.separate("netmag")
            netmag_view.free()
            netmag_view = _view
            _view = netmag_view.subset("orid == %d" % origin.orid)
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
        
    def plot_origin(self,
                    origin,
                    pre_filter=('highpass', {"freq": 2.0}),
                    resolution='c',
                    savefig=False,
                    show=True):
        gather = Gather()
        for arrival in origin.arrivals:
            try:
                gather += self.load_trace(arrival.station,
                                          arrival.channel,
                                          origin.time,
                                          origin.time + 60)
            except IOError:
                continue
        if len(gather.traces) == 0:
            return None
        try:
            gather.filter(pre_filter[0], **pre_filter[1])
        except NotImplementedError:
            return None
        fig = plt.figure(figsize=(16.5, 8.5))
        fig.suptitle("%d: %.2f %.2f %.2f\n%s" % (origin.evid,
                                                 origin.lat,
                                                 origin.lon,
                                                 origin.depth,
                                                 origin.time),
                    fontsize=22)
        ax1 = fig.add_subplot(1, 2, 1)
        #ax1 = fig.add_axes([0.0, 0.0, 0.5, 0.5])
        ax1.set_aspect('equal', adjustable='box')
        origin.plot(subplot_ax=ax1,
                    show=False,
                    cmap=mpl.cm.jet)
        ax2 = fig.add_subplot(1, 2, 2)
        #ax2 = fig.add_axes([0.5, 0.2, 0.5, 0.5])
        gather.plot("section",
                    origin.lat,
                    origin.lon,
                    float(origin.time),
                    arrivals=origin.arrivals,
                    cmap=mpl.cm.jet,
                    set_yticks_position="right",
                    show=False,
                    subplot_ax=ax2)
        xmin, xmax = ax2.get_xlim()
        ymax, ymin = ax2.get_ylim()
        ax2.set_aspect((xmax - xmin) / (ymax - ymin), adjustable='box')
        #cax = fig.add_axes([0.1, 0.1, 0.75, 0.025])
        #mpl.colorbar.ColorbarBase(cax,
        #                          cmap=mpl.cm.jet)
        plt.subplots_adjust(wspace=0.0)
        if not savefig == False:
            print "Saving to: %s" % savefig
            plt.savefig(savefig, format="png")
        if show:
            plt.show()
        else:
            return fig

    def plot_origin_dep(self,
                    origin,
                    pre_filter=('highpass', {"freq": 2.0}),
                    resolution='c',):
        lat0, lon0 = origin.lat, origin.lon
        traces = []
        for arrival in origin.arrivals:
            try:
                traces += [self.load_trace(arrival.station,
                                  arrival.channel,
                                  origin.time,
                                  origin.time + 60)]
            except IOError:
                continue
        sort_key = lambda tr: sqrt((tr.stats.station.lat - origin.lat) ** 2 +
                                   (tr.stats.station.lon - origin.lon) ** 2)
        traces = sorted(traces, key=sort_key)
        [trace.filter(pre_filter[0], **pre_filter[1]) for trace in traces]
        [trace.detrend("demean") for trace in traces]
        ntraces = len(traces)
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
        plt.figure(figsize=(16.5, 8))
        ax = plt.subplot2grid((ntraces, 2),
                              (0, 0),
                              rowspan=ntraces,
                              colspan=1)
        m = Basemap(llcrnrlon=x0 - extent,
                    llcrnrlat=y0 - extent,
                    urcrnrlon=x0 + extent,
                    urcrnrlat=y0 + extent,
                    resolution=resolution)
        m.arcgisimage(server='http://server.arcgisonline.com/arcgis',
                      service='USA_Topo_Maps')
        m.drawmapboundary()
        m.scatter(lon0, lat0, marker="*", color="r", s=100)
        m.scatter(X, Y, marker="v", color="g", s=50)
        # Plot trace data to the right of map
        set_xlabel = False
        set_xticks_label = False
        xaxis_set_visible = False
        xticklabel_fmt = None
        ax0 = plt.subplot2grid((ntraces, 2),
                               (0, 1),
                               rowspan=1,
                               colspan=1)
        traces[0].subplot(ax0,
                          xaxis_set_visible=xaxis_set_visible,
                          set_xlabel=set_xlabel,
                          set_yticks_position="right")
        for i in range(1, len(traces)):
            if i == len(traces) - 1:
                xaxis_set_visible = True
                set_xlabel = True
                set_xticks_label = True
                xticklabel_fmt = "%H:%M:%S"
            ax = plt.subplot2grid((ntraces, 2),
                                  (i, 1),
                                  rowspan=1,
                                  colspan=1,
                                  sharex=ax0)
            traces[i].subplot(ax,
                              set_xlabel=set_xlabel,
                              set_xticks_label=set_xticks_label,
                              set_yticks_position="right",
                              xaxis_set_visible=xaxis_set_visible,
                              xticklabel_fmt=xticklabel_fmt)
        plt.subplots_adjust(wspace=0.0, hspace=0.0)
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
                           ('sta', arrival.station.name),
                           ('phase', arrival.phase))
