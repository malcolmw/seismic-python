#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:02:22 2016

@author: malcolcw
"""


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


class VirtualNetwork:
    """
    .. todo::
       document this class
    """
    def __init__(self, code):
        self.code = code
        self.subnets = {}

    def __getattr__(self, name):
        if name == "stations":
            self.stations = {}
            for snet in self.subnets:
                for station in self.subnets[snet].stations:
                    if station not in self.stations:
                        self.stations[station] =\
                                self.subnets[snet].stations[station]
            return self.stations
        else:
            raise AttributeError("attribute doesn't exist")

    def add_subnet(self, subnet):
        if subnet.code not in self.subnets:
            self.subnets[subnet.code] = subnet
