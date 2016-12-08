#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:53:59 2016

@author: malcolcw
"""
import numpy as np
from math import radians, sin
import mmap
import os
import struct


class TTGrid:
    """
    This class provides query functionality for memory-mapped
    travel-time files.
    """
    def __init__(self, ttdir):
        self._initialize_mmap(ttdir)
        self.byteoffset = np.ndarray(shape=self.nodes['r'].shape)
        # jump over grid definition
        offset = 36
        for iphi in range(self.nphi):
            for itheta in range(self.ntheta):
                for ir in range(self.nr):
                    self.byteoffset[ir, itheta, iphi] = offset
                    offset += 4

#    def __del__(self):
#        print "DELETE!"
#        for station in self.mmttf:
#            for phase in self.mmttf[station]:
#                self.mmttf[station][phase].close()

    def _initialize_mmap(self, ttdir):
        mmttf = {}
        init = True
        for infile in os.listdir(ttdir):
            station, phase = infile.split(".")[:2]
            infile = open(os.path.abspath(os.path.join(ttdir, infile)), 'rb')
            mmf = mmap.mmap(infile.fileno(), 0, access=mmap.ACCESS_READ)
            if station not in mmttf:
                mmttf[station] = {}
            mmttf[station][phase] = mmf
            if init:
                init = False
                self._initialize_grid(mmf)
            else:
                nr, nlat, nlon = struct.unpack("3i", mmf.read(12))
                dr, dlat, dlon = struct.unpack("3f", mmf.read(12))
                r0, lat0, lon0 = struct.unpack("3f", mmf.read(12))
                if not nr == self.nr\
                        or not nlat == self.nlat\
                        or not nlon == self.nlon\
                        or not dr == self.dr\
                        or not dlat == self.dlat\
                        or not dlon == self.dlon\
                        or not r0 == self.r0\
                        or not lat0 == self.lat0\
                        or not lon0 == self.lon0:
                    raise ValueError("travel-time headers do not match")
        self.mmttf = mmttf

    def _initialize_grid(self, mmf):
        self.nr, self.nlat, self.nlon\
            = struct.unpack("3i", mmf.read(12))
        self.dr, self.dlat, self.dlon\
            = struct.unpack("3f", mmf.read(12))
        self.r0, self.lat0, self.lon0\
            = struct.unpack("3f", mmf.read(12))
        self.mr = self.r0 + (self.nr - 1) * self.dr
        self.mlat = self.lat0 + (self.nlat - 1) * self.dlat
        self.mlon = self.lon0 + (self.nlon - 1) * self.dlon
        self.dtheta = radians(self.dlat)
        self.dphi = radians(self.dlon)
        self.ntheta, self.nphi = self.nlat, self.nlon
        self.theta0 = radians(90 - self.lat0)
        self.phi0 = radians(self.lon0)
        r = [self.r0 + self.dr * ir for ir in range(self.nr)]
        theta = [radians(90. - self.lat0 - self.dlat * ilat)
                 for ilat in range(self.nlat)]
        phi = [radians((self.lon0 + self.dlon * ilon) % 360.)
               for ilon in range(self.nlon)]
        R, T, P = np.meshgrid(r, theta, phi, indexing='ij')
        self.nodes = {'r': R, 'theta': T, 'phi': P}

    def contains(self, r, theta, phi):
        if not self.r0 < r < self.r0 + self.dr * (self.nr - 1):
            return False
        if not self.theta0 - (self.ntheta - 1) * self.dtheta < theta < self.theta0:
            return False
        if not self.phi0 < phi < self.phi0 + (self.nphi - 1) * self.dphi:
            return False
        return True

    def get_node_tt(self, station, phase, ir, itheta, iphi):
        print station, phase, ir, itheta, iphi
        f = self.mmttf[station][phase]
        offset = self.byteoffset[ir, itheta, iphi]
        print f, offset
        f.seek(int(offset))
        return struct.unpack("f", f.read(4))[0]

    def get_proximal_node(self, r, theta, phi):
        """
        Return indices of minimal vertex of bounding cube and distance
        from proximal node along each axis.
        """
        ir0 = (r - self.r0) / self.dr
        itheta0 = (self.theta0 - theta) / self.dtheta
        iphi0 = (phi - self.phi0) / self.dphi
        delr, deltheta, delphi = ir0 % 1., itheta0 % 1., iphi0 % 1.
        return (int(ir0), int(itheta0), int(iphi0)), (delr, deltheta, delphi)

    def get_tt_cube(self, station, phase, ir0, itheta0, iphi0):
        ir1 = ir0 if ir0 == self.nr - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == self.ntheta - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == self.nphi - 1 else iphi0 + 1
        T000 = self.get_node_tt(station, phase, ir0, itheta0, iphi0)
        T100 = self.get_node_tt(station, phase, ir1, itheta0, iphi0)
        T010 = self.get_node_tt(station, phase, ir0, itheta1, iphi0)
        T110 = self.get_node_tt(station, phase, ir1, itheta1, iphi0)
        T001 = self.get_node_tt(station, phase, ir0, itheta0, iphi1)
        T101 = self.get_node_tt(station, phase, ir1, itheta0, iphi1)
        T011 = self.get_node_tt(station, phase, ir0, itheta1, iphi1)
        T111 = self.get_node_tt(station, phase, ir1, itheta1, iphi1)
        return (T000, T100, T010, T110, T001, T101, T011, T111)

    def get_tt(self, station, phase, r, theta, phi):
        index, delta = self.get_proximal_node(r, theta, phi)
        ir, itheta, iphi = index
        delr, deltheta, delphi = delta
        (T000, T100, T010, T110,
         T001, T101, T011, T111) = self.get_tt_cube(station,
                                                    phase,
                                                    ir,
                                                    itheta,
                                                    iphi)
        T00 = T000 + (T100 - T000) * delr
        T10 = T010 + (T110 - T010) * delr
        T01 = T001 + (T101 - T001) * delr
        T11 = T011 + (T111 - T001) * delr
        T0 = T00 + (T10 - T00) * deltheta
        T1 = T01 + (T11 - T01) * deltheta
        return T0 + (T1 - T0) * delphi

    def get_ttgradient(self, station, phase, r, theta, phi):
        index, delta = self.get_proximal_node(r, theta, phi)
        ir, itheta, iphi = index
        (T000, T100, T010, T110,
         T001, T101, T011, T111) = self.get_tt_cube(station,
                                                    phase,
                                                    ir,
                                                    itheta,
                                                    iphi)
        dTdr00 = T100 - T000
        dTdr10 = T110 - T010
        dTdr01 = T101 - T001
        dTdr11 = T111 - T011
        dTdr = np.mean([dTdr00, dTdr10, dTdr01, dTdr11])
        dTdt00 = T010 - T000
        dTdt10 = T110 - T100
        dTdt01 = T011 - T001
        dTdt11 = T111 - T101
        dTdt = np.mean([dTdt00, dTdt10, dTdt01, dTdt11])
        dTdp00 = T001 - T000
        dTdp10 = T101 - T100
        dTdp01 = T011 - T010
        dTdp11 = T111 - T110
        dTdp = np.mean([dTdp00, dTdp10, dTdp01, dTdp11])
        # the discretization of the travel time-field may account for
        # spherical coordinate transformation...
        return dTdr, dTdt, dTdp


def test():
    ttg = TTGrid("/home/shake/malcolcw/data/fm3d_ttimes")
    from seispy.geometry import geo2sph
    r, theta, phi = geo2sph(33.2, -116.6, 12)
    print ttg.get_ttgradient("PFO", "P", r, theta, phi)

if __name__ == "__main__":
    test()
