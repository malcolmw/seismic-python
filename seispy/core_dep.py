from copy import deepcopy
from os.path import isfile

import re

from obspy.core import read,\
                       Stream,\
                       UTCDateTime

import obspy.core

from seispy.util import verify_time
from gazelle.datascope import Dbptr,\
                              dbopen,\
                              dbSCHEMA_NAME,\
                              dbTABLE_FIELDS,\
                              dbTABLE_IS_VIEW
################
#              #
#  EXCEPTIONS  #
#              #
################

class ArgumentError(Exception):
    """
    .. todo::
       document this class
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class InitializationError(Exception):
    """
    .. todo::
       document this class
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

##########################
#                        #
#  PRIVATE BASE CLASSES  #
#                        #
##########################

class _DbParsable(object):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        print (__package__)
        pass

    def __str__(self):
        ret = "{} Instance".format(self.__class__)
        ret += "\n" + "-" * (len(str(self.__class__)) + 8) + "\n"
        width = max([len(attr) for attr in self.attributes]) + 1
        for attr in self.attributes:
            ret += "{:<{width}s} {}\n".format((attr + ':'),
                                             getattr(self, attr),
                                             width=width)
        return ret.rstrip()

class _BaseChannel:
    """
    .. todo::
       document this class
    """
    def __init__(self):
        pass

    def is_active(self, **kwargs):
        if 'start' in kwargs and 'stop' in kwargs:
            start = verify_time(kwargs['start'])
            stop = verify_time(kwargs['stop'])
            if self.ondate <= start and self.offdate >= stop:
                #print "Active: {:s} - {:s}".format(start, stop)
                return True
            else:
                #print "Inactive: {:s} - {:s}".format(start, stop)
                return False
        elif 'time' in kwargs:
            time = verify_time(kwargs['time'])
            if self.ondate <= time and self.offdate >= time:
                #print "Active: {:s} - {:s}".format(start, stop)
                return True
            else:
                #print "Inactive: {:s} - {:s}".format(start, stop)
                return False
    def _parse_Dbptr(self, dbptr):
        if not _ANTELOPE_DEFINED:
            raise InitializationError("Antelope environment not initialized")
        if not isinstance(dbptr, Dbptr):
            print type(dbptr), dbptr.__class__
            raise TypeError("expected antelope.datascope.Dbptr instance")
        if dbptr.record < 0 or dbptr.record >= dbptr.record_count:
            raise IndexError("invalid record index in antelope.datascope.Dbptr")
        for field in dbptr.query(dbTABLE_FIELDS):
            if field not in self.attributes:
                setattr(self, field, dbptr.getv(field)[0])
                self.attributes += (field,)

    def _parse_kwargs(self, kwargs):
        for kw in primary_kwargs:
            if kw not in kwargs:
                raise InitializationError("keywords {} required for "\
                        "{:s}()".format(primary_kwargs, self.__class__))
            for kw in valid_kwargs:
                if kw in kwargs:
                    setattr(self, attr, kwargs[kw])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)

#########################
#                       #
#  PUBLIC BASE CLASSES  #
#                       #
#########################

####################
#                  #
#  PUBLIC CLASSES  #
#                  #
####################

class Event(_DbParsable):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        elif 'evid' in kwargs and 'database' in kwargs:
            _db = kwargs['database']
            _evid = kwargs['evid']
            _dbptr = _db._dbptr
            _tbl_event = _dbptr.lookup(table='event')
            _tbl_event.record = _tbl_event.find("evid == {:d}".format(_evid))
            self._parse_Dbptr(_tbl_event.record)
            _tbl_origin = _dbptr.lookup(table='origin')
            _tbl_origin = _tbl_origin.subset("evid == {:d}".format(_evid))
            self.origins = []
            for origin in _tbl_origin.iter_record():
                self.origins += [Origin(database=_db, orid=origin.getv('orid')[0])]
            self.attributes += ('origins',)

class Arrival(_DbParsable):
    """
    The Arrival class is a container class for phase arrival data and
    can be initialized one of two ways.


    1. Specifying a series of keyword arguments initializing individual
       fields. If initializating via keyword arguments primary keys
       *sta*, *time*, and *iphase* must be specified.

    **OR**

    2. Passing in a seispy.antelope.datascope.Dbptr object that points
       to a record in an *arrival* table.

    The second method of initialization is intended primarily for
    internal use within the seispy package.

    :argument seispy.antelope.datascope.Dbptr args: Database pointer\
    to record in *arrival* table
    :keyword str sta: Station code
    :keyword float time: Arrival time
    :keyword str iphase: Interpreted phase
    :keyword str chan: Channel code
    :keyword float deltim: Arrival timing error
    :keyword float qual: Pick quality ('i'=impulsive, 'e'=emergent,\
                         'w'=weak)
    :raise InitializationError: if initialization method 2 is used and
                                primary keys (*sta*, *time*, and
                                *iphase*) are not specified.

    .. versionadded:: 0.0alpha
    .. codeauthor:: Malcolm White mcwhite@ucsd.edu
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        else:
            primary_kwargs = ('sta', 'time', 'iphase')
            for kw in primary_kwargs:
                if kw not in kwargs:
                    raise InitializationError("must specify 'sta', 'time', "\
                            "and 'iphase' for Arrival")
            valid_kwargs = ('sta',
                            'time',
                            'arid',
                            'jdate',
                            'stassid',
                            'chanid',
                            'chan',
                            'iphase',
                            'stype',
                            'deltim',
                            'azimuth',
                            'delaz',
                            'slow',
                            'delslo',
                            'ema',
                            'rect',
                            'amp',
                            'per',
                            'logat',
                            'clip',
                            'fm',
                            'snr',
                            'qual',
                            'auth',
                            'commid',
                            'lddate')
            for kw in valid_kwargs:
                if kw in kwargs:
                    setattr(self, attr, kwargs[kw])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)

class Blackout:
    """
    .. todo::
       document this class
    """
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class Channel(_BaseChannel):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        for attr in ('chan', 'ondate', 'offdate'):
            if attr not in kwargs:
                raise InitializationError("expected '{:s}' keyword "\
                        "argument".format(attr))
        if not isinstance(kwargs['chan'], str):
            raise TypeError("invalid type for chan argument")
        for datearg in ('ondate', 'offdate'):
            setattr(self, datearg, verify_time(kwargs[datearg]))
        self.chan = kwargs['chan']
        self.attributes = ('chan', 'ondate', 'offdate')

    def __str__(self):
        return self.chan

class ChannelSet(_BaseChannel):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        self.blackouts = ()
        if 'chans' not in kwargs:
            for chan in ('chanV, chanH1', 'chanH2'):
                if chan not in kwargs:
                    raise InitializationError("if 'chans' keyword argument not "\
                            "not specified '{:s}' keyword must be "\
                            "specified".format(chan))
        if 'chans' in kwargs:
            self.chanV = kwargs['chans'][0]
            self.chanH1 = kwargs['chans'][1]
            self.chanH2 = kwargs['chans'][2]
        else:
            self.chanV = chanV
            self.chanH1 = chanH1
            self.chanH2 = chanH2
        self.id = "{:s}:{:s}:{:s}".format(self.chanV.chan,
                                          self.chanH1.chan,
                                          self.chanH2.chan)
        self.ondate, self.offdate = float('-inf'), float('inf')
        for chan in (self.chanV, self.chanH1, self.chanH2):
            if chan.ondate > self.ondate:
                self.ondate = chan.ondate
            if chan.offdate < self.offdate:
                self.offdate = chan.offdate

    def __add__(self, other):
        if self.id != other.id:
            raise ValueError("channel set ID's do not match, cannot add")
        _self = deepcopy(self)
        ondates = sorted([_self.ondate, other.ondate] +\
                         [b.stop for b in _self.blackouts])
        offdates = sorted([_self.offdate, other.offdate] +\
                          [b.start for b in _self.blackouts])
        _self.blackouts = ()
        _self.ondate = ondates.pop(0)
        _self.offdate = offdates.pop()
        while True:
            try:
                offdate = offdates.pop(0)
                ondate = ondates.pop(0)
            except IndexError:
                break
            if ondate > offdate:
                _self.blackouts += (Blackout(start=offdate,
                                             stop=ondate),)
        return _self

    def __str__(self):
        s = "({:s}, {:s}, {:s}) :: {:s} - {:s}".format(self.chanV,
                                                       self.chanH1,
                                                       self.chanH2,
                                                       self.ondate,
                                                       self.offdate)
        if self.blackouts:
            for blackout in self.blackouts:
                s += "\nBlackout: {:s} - {:s}".format(blackout.start,
                                                      blackout.stop)
        return s

class Database:
    """
    .. todo::
       document this class
    """
    def __init__(self, *args):
        self._dbptr = dbopen(*args)
        self._schema = Schema(schema=self._dbptr.query(dbSCHEMA_NAME))
        _tbl_arrival = self._dbptr.lookup(table='arrival')
        _tmp_view = _tbl_arrival.join('assoc')
        self._srtd_arrival = _tmp_view.sort('orid')
        _tmp_view.free()
        self._grpd_arrival = self._srtd_arrival.group('orid')
        self.vnet = VirtualNetwork(database=self, vnet='ZZ')

    def close(self):
        self._dbptr.close()

    def origins(self, sort_keys=None):
        return OriginIterator(self, sort_keys)



class EventIterator:
    """
    .. todo::
       document this class
    """
    def __init__(self, database):
        self._database = database
        self._tbl_event = database._dbptr.lookup(table='event')
        self._tbl_event.record = 0

    def __iter__(self):
        return self

    def next(self):
        if self._tbl_event.record == self._tbl_event.record_count:
            raise StopIteration
        _event = Event(evid=self._tbl_event.getv('evid')[0],
                       database=database)
        self._tbl_event.record += 1
        return _event

class OriginIterator:
    """
    .. todo::
       document this class
    """
    def __init__(self, database, sort_keys):
        self._database = database
        if sort_keys:
            for key in sort_keys:
                if key not in ('lat',
                            'lon',
                            'depth',
                            'time',
                            'orid',
                            'evid',
                            'jdate',
                            'nass',
                            'ndef',
                            'grn',
                            'srn',
                            'dtype',
                            'algorithm',
                            'auth'):
                    raise ValueError("invalid value for sort_keys keyword "\
                            "argument")
        self._tbl_origin = database._dbptr.lookup(table='origin')
        if sort_keys:
            self._tbl_origin = self._tbl_origin.sort(sort_keys)
        self._tbl_origin.record = 0

    def __iter__(self):
        return self

    def next(self):
        if self._tbl_origin.record == self._tbl_origin.record_count:
            if self._tbl_origin.dbTABLE_IS_VIEW:
                self._tbl_origin.close()
            raise StopIteration
        _origin = Origin(orid=self._tbl_origin.getv('orid')[0],
                      database=self._database)
        self._tbl_origin.record += 1
        return _origin

class Network:
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'net' in kwargs and 'database' in kwargs:
            self.net = kwargs['net']
            self.attributes += ('net',)
            db = kwargs['database']
            dbptr = db._dbptr
            tbl_snetsta = dbptr.lookup(table='snetsta')
            tbl_snetsta = tbl_snetsta.subset("snet =~ /{:s}/".format(self.net))
            self.stations = ()
            for record in tbl_snetsta.iter_record():
                sta = record.getv('sta')[0]
                try:
                    self.stations += (Station(database=db, sta=sta),)
                except InitializationError as err:
                    print err.message
            self.attributes += ('stations',)
            tbl_snetsta.free()
        else:
            #implement explicit argument specification parsing
            raise InitializationError("specify 'net' and 'database' keyword "\
                    "arguments")

class Origin(_DbParsable):
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        elif len(args) == 4:
            self.lat = args[0]
            self.lon = args[1]
            self.depth = args[2]
            self.time = args[3]
            self.attributes += ('lat', 'lon', 'depth', 'time')
            for attr in ('orid', 'evid', 'jdate', 'nass', 'ndef', 'arrivals'):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)
        elif 'orid' in kwargs and 'database' in kwargs:
            _db = kwargs['database']
            _orid = kwargs['orid']
            _dbptr = _db._dbptr
            _tbl_origin = _dbptr.lookup(table='origin')
            _tbl_origin.record = _tbl_origin.find("orid == {:d}".format(_orid))
            self._parse_Dbptr(_tbl_origin)
            _grpd_arrival = _db._grpd_arrival
            _grpd_arrival.record = _grpd_arrival.find("orid == "\
                    "{:d}".format(_orid))
            self.arrivals = []
            _srtd_arrival = _db._srtd_arrival
            start, end = _grpd_arrival.get_range()
            for _srtd_arrival.record in range(start, end):
                self.arrivals += [Arrival(_srtd_arrival)]
            self.attributes += ('arrivals',)

        else:
            raise TypeError("__init__() takes exactly 1 or 5 arguments ({:d} "\
                    "given)".format(len(args)))

class Station(_DbParsable):
    """
    .. todo::
       document this class
    """
    '''
    A container class for station data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'sta' in kwargs and 'database' in kwargs:
            db = kwargs['database']
            self.sta = kwargs['sta']
            self.attributes += ('sta',)
            dbptr = db._dbptr
            tbl_site = dbptr.lookup(table='site')
            tbl_site = tbl_site.subset("sta =~ /{:s}/".format(self.sta))
            tmp = tbl_site.sort('offdate')
            tmp.record = tmp.record_count - 1
            if tmp.record < 0:
                raise InitializationError("station code '{:s}' not found in "\
                        "site table".format(self.sta))
            self.offdate = tmp.getv('offdate')[0]
            self.attributes += ('offdate',)
            tmp.free()
            tmp = tbl_site.sort('ondate')
            tmp.record = 0
            self.ondate = tmp.getv('ondate')[0]
            self.attributes += ('ondate',)
            self._blackouts = []
            if tmp.record_count > 1:
                for recno in range(tmp.record_count - 1):
                    tmp.record = recno
                    start = tmp.getv('offdate')[0]
                    tmp.record = recno + 1
                    stop = tmp.getv('ondate')[0]
                    self._blackouts += [Blackout(start, stop)]
            tmp.free()
            tmp = tbl_site.join('sitechan')
            self.channels = []
            for record in tmp.iter_record():
                chan, ondate, offdate = record.getv('chan',
                                                    'sitechan.ondate',
                                                    'sitechan.offdate')
                #REVIEW THIS
                if offdate == -1:
                    offdate = db._schema.attributes['offdate'].Null
                self.channels += [Channel(chan=chan, ondate=ondate, offdate=offdate)]
            self.attributes += ('channels',)
            tmp.free()

    def get_channels(self, **kwargs):
        channels = ()
        if 'match' in kwargs:
            expr = re.compile(kwargs['match'])
            for channel in self.channels:
                if re.match(expr, channel.chan):
                    channels += (channel,)
        else:
            channels = self.channels
        return channels

    def get_orthogonal_channels(self, **kwargs):
        channels = ()
        if 'match' in kwargs:
            expr = re.compile(kwargs['match'])
            for channel in self.channels:
                if re.match(expr, channel.chan):
                    channels += (channel,)
        else:
            channels = self.channels
        orthogonal_channels = ()
        for channel in channels:
            if channel.chan[2] == 'Z':
                expr = re.compile("{:s}[^Z]{:s}".format(channel.chan[:2], channel.chan[3:]))
                _channels = (channel,)
                for _channel in channels:
                    if re.match(expr, _channel.chan) and\
                            _channel.is_active(start=channel.ondate,
                                               stop=channel.offdate):
                        _channels += (_channel,)
                if len(_channels) == 1:
                    continue
                elif len(_channels) == 3:
                    channel_set = ChannelSet(chans=_order_orthogonal_channels(_channels))
                    orthogonal_channels += (channel_set,)
                else:
                    channel_set = ChannelSet(chans=_squash_channel_set(_channels))
                    orthogonal_channels += (channel_set,)
        _orthogonal_channels = []
        if len(orthogonal_channels) > 1:
            for i in range(len(orthogonal_channels)):
                flag = False
                for j in range(len(_orthogonal_channels)):
                    if orthogonal_channels[i].id == _orthogonal_channels[j].id:
                        _orthogonal_channels[j] += orthogonal_channels[i]
                        flag = True
                        break
                if flag:
                    continue
                else:
                    _orthogonal_channels += [orthogonal_channels[i]]
        return tuple(_orthogonal_channels)

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
                #try:
                #    import os
                #    import sys
                #    sys.path.append("{:s}/data/python".format(os.environ['ANTELOPE']))
                #except ImportError:
                #    raise ImportError("$ANTELOPE environment variable not defined")
                #from antelope.datascope import Dbptr,\
                #                            dbTABLE_NAME
                if isinstance(args[0], Dbptr):
                    dbptr = args[0]
                    if dbptr.query(dbTABLE_NAME) == 'wfdisc':
                        if dbptr.record >= 0 and dbptr.record < dbptr.record_count:
                            tr = read(dbptr.filename()[1])[0]
                            self.stats = tr.stats
                            self.data = tr.data
                        else:
                            raise ValueError("Dbptr.record out of range")
                    else:
                        raise ValueError("Dbptr argument received by "\
                                "__init__() must point to 'wfdisc' table "\
                                "(Dbptr points to '{:s}' table)".format(dbptr.query(dbTABLE_NAME)))
                else:
                    raise TypeError("Unable to process single argument passed "\
                            "to __init__(): {:s}".format(args[0]))
        else:
            if 'station' not in kwargs or\
                    'channel' not in kwargs or\
                    'starttime' not in kwargs or\
                    'endtime' not in kwargs:
                raise ArgumentError("__init__() expected 'station', 'channel',"\
                        " 'starttime' and 'endtime' keyword arguments")
            if not isinstance(kwargs['starttime'], UTCDateTime) and\
                    not isinstance(kwargs['starttime'], float) and\
                    not isinstance(kwargs['starttime'], int):
                raise TypeError("__init__() keyword argument 'starttime' must "\
                        "be of type 'UTCDateTime', 'float' or 'int'")
            if not isinstance(kwargs['endtime'], UTCDateTime) and\
                   not isinstance(kwargs['endtime'], float) and\
                    not isinstance(kwargs['endtime'], int):
                raise TypeError("__init__() keyword argument 'endtime' must "\
                        "be of type 'UTCDateTime', 'float' or 'int'")
            if not isinstance(kwargs['station'], str):
                raise TypeError("__init__() keyword argument 'station' must "\
                        "be of type 'str'")
            if not isinstance(kwargs['channel'], str):
                raise TypeError("__init__() keyword argument 'channel' must "\
                        "be of type 'str'")
            if 'database_path' in kwargs:
                if not isfile("{:s}.wfdisc".format(kwargs['database_path'])):
                    raise InitializationError("wfdisc does not exist "\
                            "{:s}.wfdisc".format(kwargs['database_path']))
                #import os
                #import sys
                #try:
                #    sys.path.append("{:s}/data/python".format(os.environ['ANTELOPE']))
                #except ImportError:
                #    raise ImportError("$ANTELOPE environment variable not set")
                #from antelope.datascope import closing,\
                #                                dbopen,\
                #                                dbTABLE_IS_VIEW
                dbptr = dbopen(kwargs['database_path'], 'r')
            elif 'database_pointer' in kwargs and\
                    isinstance(kwargs['database_pointer'], Dbptr):
                dbptr = dbopen(kwargs['database_path'], 'r')
            else:
                raise ArgumentError("__init__() expected either "\
                        "'database_path' or 'database_pointer' keyword "\
                        "argument")
            dbptr = dbptr.lookup(table='wfdisc')
            if isinstance(kwargs['starttime'], float) or isinstance(kwargs['starttime'], int):
                kwargs['starttime'] = UTCDateTime(kwargs['starttime'])
            if isinstance(kwargs['endtime'], float) or isinstance(kwargs['endtime'], int):
                kwargs['endtime'] = UTCDateTime(kwargs['endtime'])
            dbptr = dbptr.subset("sta =~ /{:s}/ && chan =~ /{:s}/ && "\
                    "endtime > _{:s}_ && time < _{:s}_".format(kwargs['station'],
                                                               kwargs['channel'],
                                                               kwargs['starttime'],
                                                               kwargs['endtime']))
            if dbptr.record_count == 0:
                raise InitializationError("__init__() found no data for "\
                        "{:s}:{:s} {:s}-{:s}".format(kwargs['station'],
                                                     kwargs['channel'],
                                                     kwargs['starttime'],
                                                     kwargs['endtime']))
            st = Stream()
            for record in dbptr.iter_record():
                st += read(record.filename()[1],
                           starttime=kwargs['starttime'],
                           endtime=kwargs['endtime'])[0]
            st.merge()
            tr = st[0]
            self.stats = tr.stats
            self.data = tr.data

class VirtualNetwork:
    """
    .. todo::
       document this class
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'database' in kwargs and 'vnet' in kwargs:
            db = kwargs['database']
            self.vnet = kwargs['database']
            self.attributes += ('vnet',)
            tbl_snetsta = db._dbptr.lookup(table='snetsta')
            tbl_snetsta = tbl_snetsta.sort('snet', unique=True)
            self.subnets = ()
            for record in tbl_snetsta.iter_record():
                self.subnets += (Network(database=db,
                                          net=record.getv('snet')[0]),)
            tbl_snetsta.free()
            self.attributes += ('subnets',)
        else:
            raise InitializationError("specify 'database' and 'vnet' keyword "\
                    "arguments")

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
    if channels[1].chan[2] == 'E' and channels[2].chan[2] == 'N':
        channels = (channels[0], channels[2], channels[1])
    elif channels[1].chan[2] == 'N' and channels[2].chan[2] == 'E':
        pass
    else:
        try:
            comp1 = int(channels[1].chan[2])
            comp2 = int(channels[2].chan[2])
        except ValueError:
            raise ValueError("could not order orthogonal channels")
        if comp1 > comp2:
            channel2, channel3 = channels[2], channels[1]
        else:
            channel2, channel3 = channels[1], channels[2]
        channels = (channels[0], channel2, channel3)
    return channels

def _squash_channel_set(channels):
    """
    .. todo::
       document this function
    """
    prefix = channels[0].chan[:2]
    for channel in channels:
        if channel.chan[:2] != prefix:
            raise ValueError("{:s} does not form an orthogonal set with "\
                    "{:s}".format(channel[:2], prefix))
    channel1, channel2, channel3 = (), (), ()
    for channel in channels:
        if channel.chan[2] == 'Z':
            channel1 += (channel,)
        elif channel.chan[2] == 'N':
            channel2 += (channel,)
        elif channel.chan[2] == 'E':
            channel3 += (channel,)
    if channel2 == () and channel3 == ():
        for channel in channels:
            if channel.chan[2] != 'Z':
                if channel2 == ():
                    channel2 = (channel,)
                elif channel3 == ():
                    channel3 = (channel,)
                elif int(channel.chan[2]) < int(channel2[0].chan[2]):
                    channel3 = channel2
                    channel2 = (channel,)
                elif int(channel.chan[2]) == int(channel2[0].chan[2]):
                    channel2 += (channel,)
                elif int(channel.chan[2]) < int(channel3[0].chan[2]):
                    channel3 = (channel,)
                elif int(channel.chan[2]) == channel3[0].chan[2]:
                    channel3 += (channel,)
    if len(channel1) == 1:
        channel1 = channel1[0]
    else:
        channel1 = _get_priority_channel(channel1)
    if len(channel2) == 1:
        channel2 = channel2[0]
    else:
        channel2 = _get_priority_channel(channel2)
    if len(channel3) == 1:
        channel3 = channel3[0]
    else:
        channel3 = _get_priority_channel(channel3)
    return channel1, channel2, channel3

def _get_priority_channel(channels):
    """
    .. todo::
       document this function
    """
    channel = None
    for _channel in channels:
        if channel == None:
            channel = _channel
            if channel.chan[3:] == '':
                break
        elif _channel.chan[3:] == '':
            channel = _channel
            break
        else:
            try:
                _loc = int(_channel.chan[4:])
                loc = int(channel.chan[4:])
            except ValueError:
                print "Not sure how to handle channel {:s}, "\
                        "skipping".format(_channel)
                continue
            if _loc < loc:
                channel = _channel
    return channel
