#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:01:25 2016

@author: malcolcw
"""
import seispy as sp
import re

logger = sp.log.initialize_logging(__name__)

class Channel:
    """
    .. todo::
       document this class
    """
    def __init__(self, code, ondate, offdate):
        self.code = code
        self.ondate = sp.util.validate_time(ondate)
        self.offdate = sp.util.validate_time(offdate)
        self.inactive_periods = ()
        self.sample_rates = {'E': 0, 'H': 1, 'B': 2, 'L': 3}
        self.instruments = {'H': 0, 'N': 1}
        self.components = {'Z': 0, 'N': 1, 'E': 2, '1': 3, '2': 4}

    def __str__(self):
        return "Channel: "\
        + self.code\
        + " "\
        + str(self.ondate)\
        + " "\
        + str(self.offdate)\

    def __lt__(self, other):
        if self.sample_rates[self.code[0]] < self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] < self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] < self.components[other.code[2]]:
            return True
        else:
            return False

    def __le__(self, other):
        if self.sample_rates[self.code[0]] <= self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] <= self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] <= self.components[other.code[2]]:
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
        if self.sample_rates[self.code[0]] > self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] > self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] > self.components[other.code[2]]:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.sample_rates[self.code[0]] >= self.sample_rates[other.code[0]]:
            return True
        elif self.instruments[self.code[1]] >= self.instruments[other.code[1]]:
            return True
        elif self.components[self.code[2]] >= self.components[other.code[2]]:
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
    def __init__(self, channels):
        self.chanV = channels[0]
        self.chanH1 = channels[1]
        self.chanH2 = channels[2]
        self.id = "%s:%s:%s" % (self.chanV.code,
                                self.chanH1.code,
                                self.chanH2.code)

    def __iter__(self):
        self.index = 0
        return self

    def __str__(self):
        return self.id

    def next(self):
        if self.index > 2:
            raise StopIteration()
        elif self.index == 0:
            self.index += 1
            return self.chanV
        elif self.index == 1:
            self.index += 1
            return self.chanH1
        elif self.index == 2:
            self.index += 1
            return self.chanH2
        

class Station(object):
    def __init__(self,
                 name,
                 lon,
                 lat,
                 elev,
                 network,
                 ondate=-1,
                 offdate=-1):
        self.name = name
        self.lon = lon % 360.
        self.lat = lat
        self.elev = elev
        self.network = network
        self.ondate = sp.util.validate_time(ondate)
        self.offdate = sp.util.validate_time(offdate)
        self.channels = {}

    def __str__(self):
        return "Station: " + self.name

    def add_channel(self, channel):
        for channel0 in self.channels:
            if channel == self.channels[channel0]:
                self.channels[channel0].update(channel)
                return
        self.channels[channel.code] = channel

    def get_channels(self, match=None):
        channels = ()
        if match:
            expr = re.compile(match)
            for channel in self.channels:
                if re.match(expr, self.channels[channel].code):
                    channels += (self.channels[channel],)
        else:
            channels = [self.channels[channel] for channel in self.channels]
        return channels

    def get_channel_set(self, code):
        """
        A method to return 3-component channel sets.

        :argument str code: 2-character string indicating channel set
                            sample rate and instrument type
        :return tuple: a sorted tuple of 3 channels
        """
        channels = (self.channels[code],)
        for channel in self.channels:
            channel = self.channels[channel]
            if channel.code[2] != code[2]\
                    and channel.code[2] in ("Z", "N", "E", "1", "2")\
                    and channel.code[:2] == code[:2]\
                    and channel.code[3:] == code[3:]:
                channels += (channel,)
        return ChannelSet(sorted(channels))


class TimeSpan(object):
    def __init__(self, starttime, endtime):
        self.starttime = sp.util.validate_time(starttime)
        self.endtime = sp.util.validate_time(endtime)

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
