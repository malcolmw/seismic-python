from seispy.core.exceptions import InitializationError
from seispy.util.time import verify_time

class Channel:
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

class ChannelSet:
    def __init__(self, *args, **kwargs):
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
        self.ondate, self.offdate = float('-inf'), float('inf')
        for chan in (self.chanV, self.chanH1, self.chanH2):
            if chan.ondate > self.ondate:
                self.ondate = chan.ondate
            if chan.offdate < self.offdate:
                self.offdate = chan.offdate

    def __str__(self):
        return "({:s}, {:s}, {:s}) :: {:s} - {:s}".format(self.chanV,
                                                          self.chanH1,
                                                          self.chanH2,
                                                          self.ondate,
                                                          self.offdate)
