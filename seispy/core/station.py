from seispy.core.channel import Channel,\
                                ChannelSet
from seispy.core.exceptions import ArgumentError,\
                                   InitializationError
from seispy.core.dbparsable import DbParsable
from seispy.util.time import verify_time

import re

class Station(DbParsable):
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
                    if re.match(expr, _channel.chan):
                        _channels += (_channel,)
                if len(_channels) == 1:
                    continue
                elif len(_channels) == 3:
                    channel_set = ChannelSet(chans=order_orthogonal_channels(_channels))
                    orthogonal_channels += (channel_set,)
                else:
                    channel_set = ChannelSet(chans=squash_channel_set(_channels))
                    orthogonal_channels += (channel_set,)
        return orthogonal_channels


#    def is_station_active(self, *args, **kwargs):
#        if len(args) == 0:
#            raise ArgumentError("at least 1 argument required")
#        time = verify_time(args[0])
#        if len(args) == 1:
#            if time < self._
#            for blackout in self._blackouts:
#                if time > blackout.start and time < blackout.stop:
#                    return False
#            return True
#        else:
#            start = time
#            stop = verify_time(args[1])
#            for blackout in self._blackouts:
#                if (start > blackout.start and start < blackout.stop) or\
#                        (stop > blackout.start and stop < blackout.stop):
#                    return False
#            return True

#    def is_channel_active(self, *args, **kwargs):
#        if len(args) == 1:
#            time = args[0]
#            if not isinstance(time, UTCDateTime) and\
#                    not isinstance(time, float) and\
#                    not isinstance(time, int):
#                raise TypeError("invalid type for time argument")
#            if not isinstance(time, UTCDateTime):
#                time = UTCDateTime(time)

class Blackout:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

def order_orthogonal_channels(channels):
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

def squash_channel_set(channels):
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
        channel1 = get_priority_channel(channel1)
    if len(channel2) == 1:
        channel2 = channel2[0]
    else:
        channel2 = get_priority_channel(channel2)
    if len(channel3) == 1:
        channel3 = channel3[0]
    else:
        channel3 = get_priority_channel(channel3)
    return channel1, channel2, channel3

def get_priority_channel(channels):
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
