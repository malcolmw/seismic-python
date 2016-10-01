from copy import deepcopy
import re

import matplotlib.pyplot as plt
import obspy
from obspy.core import read,\
                       Stream

from seispy.signal.detect import detectS as _detectS_cc
from seispy.util import validate_time
from gazelle.datascope import Dbptr,\
                              dbTABLE_NAME

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
    def __init__(self, code, ondate, offdate):
        self.code = code
        self.ondate = validate_time(ondate)
        self.offdate = validate_time(offdate)
        self.inactive_periods = ()
        self.sample_rates = {'E': 0, 'H': 1, 'B': 2, 'L': 3}
        self.instruments = {'H': 0, 'N': 1}
        self.components = {'Z': 0, 'N': 1, 'E': 2, '1': 3, '2': 4}

    def __str__(self):
        return "Channel: " + self.code + " " + str(self.ondate) + " " + str(self.offdate)

    def __lt__(self, other):
        if self.sample_rates[self.code[0]] <  self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] <  self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] <  self.components[other.code[2]]:
            return True
        else:
            return False
        
    def __le__(self, other):
        if self.sample_rates[self.code[0]] <=  self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] <=  self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] <=  self.components[other.code[2]]:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.code == other.code:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.code == other.code:
            return False
        else:
            return True

    def __gt__(self, other):
        if self.sample_rates[self.code[0]] >  self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] >  self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] >  self.components[other.code[2]]:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.sample_rates[self.code[0]] >=  self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] >=  self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] >=  self.components[other.code[2]]:
            return True
        else:
            return False

    def is_active(self, time):
        for inactive_period in self.inactive_periods:
            if inactive_period.starttime <= time <= inactive_period.endtime:
                return False
        return self.ondate <= time <= self.offdate

    def update(self, channel):
        if channel.ondate < self.ondate:
            ondate0 = channel.ondate
            minor_ondates = [self.ondate]
        else:
            ondate0 = self.ondate
            minor_ondates = [channel.ondate]
        minor_ondates += [ip.endtime for ip in self.inactive_periods]
        if channel.offdate < self.offdate:
            offdate0 = self.offdate
            minor_offdates = [channel.offdate]
        else:
            offdate0 = channel.offdate
            minor_offdates = [self.offdate]
        minor_offdates += [ip.starttime for ip in self.inactive_periods]
        self.ondate = ondate0
        self.offdate = offdate0
        self.inactive_periods = ()
        for j in range(len(minor_offdates)):
            self.inactive_periods += (TimeSpan(minor_offdates[j],
                                               minor_ondates[j]),)

class ChannelSet:
    """
    .. todo::
       document this class
    """
    def __init__(self, *args):
        if len(args) == 1:
            self.chanV = args[0]
            self.chanH1 = args[1]
            self.chanH2 = args[2]
        else:
            self.chanV = args[0][0]
            self.chanH1 = args[0][1]
            self.chanH2 = args[0][2]
        self.id = "%s:%s:%s".format(self.chanV.code,
                                    self.chanH1.code,
                                    self.chanH2.code)

class Detection(object):
    def __init__(self, station, channel, time, label):
        self.station = station
        self.channel = channel
        self.time = validate_time(time)
        self.label = label

class Gather3C(obspy.core.Stream):
    """
    .. todo::
        Document this class.
    .. warning::
       This constructor for this class assumes traces argument is in V,
       H1, H2 order.
    """
    def __init__(self, traces):
        # This call may need to pass a deepcopy of traces argument
        super(self.__class__, self).__init__(traces=traces)
        self.V = self[0]
        self.H1 = self[1]
        self.H2 = self[2]
        self.stats = deepcopy(traces[0].stats)
        channel_set = [tr.stats.channel for tr in traces]
        self.stats.channel = "%s:%s%s%s" % (channel_set[0][:2],
                                            channel_set[0][2],
                                            channel_set[1][2],
                                            channel_set[2][2])
        self.stats.channel_set = channel_set
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
        self.detections += [Detection(self.stats.station,
                                      self.stats.channel,
                                      self.stats.starttime + lag,
                                      'S')]

    #def plot(self):
    #    self.fig = plt.figure()
    #    time = [float(self.stats.starttime + i * self.stats.delta)\
    #            for i in range(self.stats.npts)]
    #    print time
    #    ax1 = self.fig.add_subplot(3, 1, 1)
    #    ax1.plot(time, self.V.data)
    #    ax2 = self.fig.add_subplot(3, 1, 2)
    #    ax2.plot(time, self.H1.data)
    #    ax3 = self.fig.add_subplot(3, 1, 3)
    #    ax3.plot(time, self.H2.data)
    #    self._plot_set_x_ticks()
    #    plt.show()

    #def _plot_set_x_ticks(self):
    #    #self.fig.subplots_adjust(hspace=0)
    #    for ax in self.fig.axes[:-1]:
    #        plt.setp(ax.get_xticklabels(), visible=False)
    #    ax = self.fig.axes[-1]
    #    ax.xaxis_date()
    #    locator = AutoDateLocator(minticks=3, maxticks=6)
    #    locator.intervald[MINUTELY] = [1, 2, 5, 10, 15, 30]
    #    locator.intervald[SECONDLY] = [1, 2, 5, 10, 15, 30]
    #    #ax.xaxis.set_major_formatter(ObsPyAutoDateFormatter(locator))
    #    #ax.xaxis.set_major_formatter(AutoDateFormatter(locator))
    #    ax.xaxis.set_major_locator(locator)
    #    plt.setp(ax.get_xticklabels(), fontsize='small')

class Network:
    """
    .. todo::
       document this class
    """
    def __init__(self, code):
        self.code = code
        self.stations = {}

    def __str__(self):
        return "Network: " + self.code

    def add_station(self, station):
        if station.name not in self.stations:
            self.stations[station.name] = station


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

class TimeSpan(object):
    def __init__(self, starttime, endtime):
        self.starttime = validate_time(starttime)
        self.endtime = validate_time(endtime)

class Station(object):
    def __init__(self, name, lon, lat, elev, ondate=-1, offdate=-1):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.elev = elev
        self.ondate = validate_time(ondate)
        self.offdate = validate_time(offdate)
        self.channels = ()

    def __str__(self):
        return "Station: " + self.name

    def add_channel(self, channel):
        for channel0 in self.channels:
            if channel == channel0:
                channel0.update(channel)
                return
        self.channels += (channel,)

    def get_channels(self, match=None):
        channels = ()
        if match:
            expr = re.compile(match)
            for channel in self.channels:
                if re.match(expr, channel.code):
                    channels += (channel,)
        else:
            channels = self.channels
        return channels

    def get_channel_set(self, code):
        """
        A method to return 3-component channel sets.

        :argument str code: 2-character string indicating channel set
                            sample rate and instrument type
        :return tuple: a sorted tuple of 3 channels
        """
        channels = ()
        for channel in self.channels:
            if channel.code[:2] == code:
                channels += (channel,)
        return sorted(channels)

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
                    raise ValueError("invalid keyword arguments")
            if not ("database_pointer" in kwargs or "database_path" in kwargs):
                    raise ValueError("invalid keyword arguments - specify database")
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
                raise ValueError("invalid keyword arguments")
            dbptr = dbptr.lookup(table='wfdisc')
            dbptr = dbptr.subset("sta =~ /%s/ && chan =~ /%s/ && "\
                    "endtime > _%f_ && time < _%f_" % (kwargs['station'],
                                                       kwargs['channel'],
                                                       kwargs['starttime'],
                                                       kwargs['endtime']))
            if dbptr.record_count == 0:
                raise IOError("no data found")
            st = Stream()
            for record in dbptr.iter_record():
                st += read(record.filename()[1],
                           starttime=starttime,
                           endtime=endtime)[0]
            st.merge()
            tr = st[0]
            self.stats = tr.stats
            self.data = tr.data

    def plot(self):
        fig = plt.figure()
        time = [float(self.stats.starttime + i * self.stats.delta)\
                for i in range(self.stats.npts)]
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(time, self.data)
        plt.show()

class VirtualNetwork:
    """
    .. todo::
       document this class
    """
    def __init__(self, code):
        self.code = code
        self.subnets = {}

    def add_subnet(self, subnet):
        if subnet.code not in self.subnets:
            self.subnets[subnet.name] = subnet

#######################
#                     #
#  PRIVATE FUNCTIONS  #
#                     #
#######################

def _order_orthogonal_channels(channels):
    """
    .. todo::
       document this function
    """
    if channels[1].code[2] == 'E' and channels[2].code[2] == 'N':
        channels = (channels[0], channels[2], channels[1])
    elif channels[1].code[2] == 'N' and channels[2].code[2] == 'E':
        pass
    else:
        try:
            comp1 = int(channels[1].code[2])
            comp2 = int(channels[2].code[2])
        except ValueError:
            raise ValueError("could not order orthogonal channels")
        if comp1 > comp2:
            channel2, channel3 = channels[2], channels[1]
        else:
            channel2, channel3 = channels[1], channels[2]
        channels = (channels[0], channel2, channel3)
    return channels
