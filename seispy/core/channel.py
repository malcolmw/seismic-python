from seispy.core.blackout import Blackout
from seispy.core.exceptions import InitializationError
from seispy.util.stime import verify_time

from copy import deepcopy
class _BaseChannel:
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

class Channel(_BaseChannel):
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
