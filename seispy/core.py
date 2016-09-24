from seispy.util import validate_time

class Arrival(object):
    def __init__(self, sta, time, phase, arid=-1):
        self.sta = sta
        self.time = time
        self.phase = phase
        self.arid = arid

class Channel:
    """
    .. todo::
       document this class
    """
    def __init__(self, chan, ondate, offdate):
        self.chan = chan
        self.ondate = ondate
        self.offdate = offdate

    def __str__(self):
        return self.chan

class Gather3C(obspy.core.Stream):
    """
    .. todo::
        Document this class.
    .. warning::
       This constructor for this class assumes traces argument is in V,
       H1, H2 order.
    """
    def __init__(self,
                 traces,
                 station,
                 channel_set,
                 starttime,
                 endtime):
        # This call may need to pass a deepcopy of traces argument
        super(self.__class__, self).__init__(traces=traces)
        self.stats = deepcopy(traces[0].stats)
        self.stats.channel = channel_set
        self.V = self[0]
        self.H1 = self[1]
        self.H2 = self[2]
        self.detections = []

    def detectS(self, cov_twin=3.0, k_twin=1.0):
        output = _detectS_cc(self.V.data,
                             self.H1.data,
                             self.H2.data,
                             cov_twin,
                             self.stats.delta,
                             k_twin)
        lag1, lag2, snr1, snr2, pol_fltr, S1, S2, K1, K2 = output
        # Checking for the various possible pick results
        if lag1 > 0 and lag2 > 0:
            if snr1 > snr2:
                lag = lag1
                snr = snr1
                chan = self.H1.stats.channel
            else:
                lag = lag2
                snr = snr2
                chan = self.H2.stats.channel
        elif lag1 > 0:
            lag = lag1
            snr = snr1
            chan = self.H1.stats.channel
        elif lag2 > 0:
            lag = lag2
            snr = snr2
            chan = self.H2.stats.channel
        else:
            return
        print "DETECTION FOUND"
        self.detections += [Detection(chan=chan,
                                      filter="NULL",
                                      sta=self.stats.station,
                                      state="dS",
                                      time=self.stats.starttime + lag)]

    def plot(self):
        self.fig = plt.figure()
        time = [float(self.stats.starttime + i * self.stats.delta)\
                for i in range(self.stats.npts)]
        print time
        ax1 = self.fig.add_subplot(3, 1, 1)
        ax1.plot(time, self.V.data)
        ax2 = self.fig.add_subplot(3, 1, 2)
        ax2.plot(time, self.H1.data)
        ax3 = self.fig.add_subplot(3, 1, 3)
        ax3.plot(time, self.H2.data)
        self._plot_set_x_ticks()
        plt.show()

    def _plot_set_x_ticks(self):
        #self.fig.subplots_adjust(hspace=0)
        for ax in self.fig.axes[:-1]:
            plt.setp(ax.get_xticklabels(), visible=False)
        ax = self.fig.axes[-1]
        ax.xaxis_date()
        locator = AutoDateLocator(minticks=3, maxticks=6)
        locator.intervald[MINUTELY] = [1, 2, 5, 10, 15, 30]
        locator.intervald[SECONDLY] = [1, 2, 5, 10, 15, 30]
        #ax.xaxis.set_major_formatter(ObsPyAutoDateFormatter(locator))
        #ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
        ax.xaxis.set_major_locator(locator)
plt.setp(ax.get_xticklabels(), fontsize='small')

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
    def __init__(self, name, lon, lat, elev, ondate=-1, offdate=-1):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.elev = elev
        self.ondate = validate_time(ondate)
        self.offdate = validate_time(offdate)

class Trace(obspy.core.Trace):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], str) and isfile(args[0]):
                tr = read(args[0])[0]
                self.stats = tr.stats
                self.data = tr.data
            else:
                if isinstance(args[0], Dbptr):
                    dbptr = args[0]
                    if dbptr.query(dbTABLE_NAME) == 'wfdisc':
                        if dbptr.record >= 0 and dbptr.record < dbptr.record_count:
                            tr = read(dbptr.filename()[1])[0]
                            self.stats = tr.stats
                            self.data = tr.data
                        else:
                            raise ValueError("invalid record value: %d" % dbptr.record)
                    else:
                        raise ValueError("invalid table value: %d" % dbptr.table)
                else:
                    raise TypeError("invalid type: %s" % type(args[0]))
        else:
            mandatory_kwargs = ('station', 'channel', 'starttime', 'endtime')
            for kw in mandatory_kwargs:
                if kw not in kwargs:
                    raise ArgumentError("missing keyword argument: %s" % kw)
            starttime = validate_time(kwargs['starttime'])
            endtime = validate_time(kwargs['endtime'])
            if not isinstance(kwargs['station'], str):
                raise TypeError("invalid type: %s" % type(kwargs['station']))
            if not isinstance(kwargs['channel'], str):
                raise TypeError("inavlid type: %s" % type(kwargs['channel']))
            if 'database_path' in kwargs:
                if not isfile("%s.wfdisc" % kwargs['database_path']):
                    raise IOError("file not found: %s" % kwargs['database_path'])
                dbptr = dbopen(kwargs['database_path'], 'r')
            elif 'database_pointer' in kwargs and\
                    isinstance(kwargs['database_pointer'], Dbptr):
                dbptr = kwargs['database_pointer']
            else:
                raise ArgumentError("missing keyword argument: database_path/database_pointer")
            dbptr = dbptr.lookup(table='wfdisc')
            dbptr = dbptr.subset("sta =~ /{:s}/ && chan =~ /{:s}/ && "\
                    "endtime > _{:s}_ && time < _{:s}_".format(kwargs['station'],
                                                               kwargs['channel'],
                                                               kwargs['starttime'],
                                                               kwargs['endtime']))
            if dbptr.record_count == 0:
                raise IOError("no data found")
            st = Stream()
            for record in dbptr.iter_record():
                st += read(record.filename()[1],
                           starttime=starttime
                           endtime=endtime)[0]
            st.merge()
            tr = st[0]
            self.stats = tr.stats
            self.data = tr.data
