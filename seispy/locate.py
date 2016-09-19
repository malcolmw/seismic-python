from math import radians
import mmap
import os.path
import struct

import numpy as np

HDR_OFST = 36

def Locator(object):
    def __init__(self, tt_dir):
        self.tt_dir = tt_dir

    def relocate(self, origin):
        self.mmttf, self.grid = self._initialize_mmap(origin)
        grid = self.grid
        r = [grid['r0'] + grid['dr'] * ir for ir in range(grid['nr'])]
        theta = [radians(90. - grid['lat0'] + grid['dlat'] * ilat)\
                for ilat in range(grid['nlat'])]
        phi = [radians((grid['lon0'] + grid['dlon'] * ilon) % 360.)\
                for ilon in range(grid['nlon'])]
        R, T, P = np.meshgrid(r, theta, phi, indexing='ij')
        self.nodes = {'r': R, 'theta': T, 'phi': P}
        r0, theta0, phi0, t0 = self._grid_search(origin)
        r0, theta0, phi0, t0 = self._subgrid_inversion(r0, theta0, phi0, t0,\
                                                       origin.arrivals)

    def _get_tt(self, arrival, ir, itheta, iphi):
        f = self.mmttf[arrival.sta.name][arrival.phase]
        nr = self.nodes['r'].shape[0]
        ntheta = self.nodes['theta'].shape[1]
        iphi = iphi - 1 if iphi > 0 else 0
        itheta = itheta - 1 if itheta > 0 else 0
        offset =    ( nr * ntheta * iphi\
                    + nr * itheta\
                    + ir)\
                * 4\
                + HDR_OFST
        f.seek(offset)
        return struct.unpack("f", f.read(4))

    def _grid_search(self, origin):
        nr = self.nodes['r'].shape[0]
        ntheta = self.nodes['theta'].shape[1]
        nphi = self.nodes['phi'].shape[2]
        best_fit = float('inf')
        for (ir, itheta, iphi)\
                in [(i, j, k) for i in range(nr)\
                              for j in range(ntheta)\
                              for k in range(nphi)]:
            at = [arr.time for arr in origin.arrivals]
            tt = [self._get_tt(arr, ir, itheta, iphi) for arr in arrivals]
            ots = [at[i] - tt[i] for i in range(len(at))]
            ot = np.mean(ots)
            misfit = sum([abs((ot + tt[i]) - at[i]) for i in range(len(at))])
            if misfit < best_fit:
                best_fit = misfit
                ir0, itheta0, iphi0, t0 = ir, itheta, iphi, ot
        return self.nodes['r'][ir0, itheta0, iphi0],\
               self.nodes['theta'][ir0, itheta0, iphi0],\
               self.nodes['phi'][ir0, itheta0, iphi0],\
               ot0
            
    def _initialize_mmap(self, origin):
        mmttf, grid = {}, None
        for arrival in origin.arrivals:
            sta = arrival.sta
            if sta.name not in mmttf:
                mmttf[sta.name] = {}
            f = open(os.path.abspath(os.path.join(self.tt_dir, "%s.%s.tt"\
                    % (sta.name, arrival.phase)), 'rb'))
            mm = mmap.mmap(f.fileno(), 0)
            mmttf[sta.name][arrival.phase] = mm
            if not grid:
                grid = {}
                grid['nr'], grid['nlat'], grid['nlon']\
                        = struct.unpack("3i", mm.read(12))
                grid['dr'], grid['dlat'], grid['dlon']\
                        = struct.unpack("3f", mm.read(12))
                grid['r0'], grid['lat0'], grid['lon0']\
                        = struct.unpack("3f", mm.read(12))
            else:
                nr, nlat, nlon = struct.unpack("3i", mm.read(12))
                dr, dlat, dlon = struct.unpack("3f", mm.read(12))
                r0, lat0, lon0 = struct.unpack("3f", mm.read(12))
                if not nr == grid['nr']\
                        or not nlat == grid['nlat']\
                        or not nlon == grid['nlon']\
                        or not dr == grid['dr']\
                        or not dlat == grid['dlat']\
                        or not dlon == grid['dlon']\
                        or not r0 == grid['r0']\
                        or not lat0 == grid['lat0']\
                        or not lon0 == grid['lon0']:
                    raise ValueError("travel-time headers do not match")
        return mmttf, grid

    def _subgrid_inversion(r0, theta0, phi0, t0, arrivals):
        ir0 = (r0 - self.nodes['r'][0, 0, 0]) / self.grid['dr']
        itheta0 = abs(theta0 - self.nodes['theta'][0, 0, 0])\
                / radians(self.grid['dlat'])
        iphi0 = (phi0 - self.nodes['phi'][0, 0, 0]) / radians(self.grid['dphi'])
        delr = ir0 % 1
        deltheta = itheta0 % 1
        delphi = iphi0 % 1
        ir1 = ir0 if ir0 == self.grid['nr'] - 1 else ir0 + 1
        itheta1 = ithetar0 if itheta0 == self.grid['ntheta'] - 1 else itheta0 + 1
        iphi1 = iphir0 if iphi0 == self.grid['nphi'] - 1 else iphi0 + 1
        D = np.empty(shape=(len(arrivals), 4))
        res = np.empty(shape=(len(arrivals),))
        for i  in range(len(arrivals)):
            arrival = arrivals[i]
            V000 = self._get_tt(arrival, ir0, itheta0, iphi0)
            V100 = self._get_tt(arrival, ir1, itheta0, iphi0)
            V010 = self._get_tt(arrival, ir0, itheta1, iphi0)
            V110 = self._get_tt(arrival, ir1, itheta1, iphi0)
            V001 = self._get_tt(arrival, ir0, itheta0, iphi1)
            V101 = self._get_tt(arrival, ir1, itheta0, iphi1)
            V011 = self._get_tt(arrival, ir0, itheta1, iphi1)
            V111 = self._get_tt(arrival, ir1, itheta1, iphi1)
            dVdr00 = V100 - V000
            dVdr10 = V110 - V010
            dVdr01 = V101 - V001
            dVdr11 = V111 - V011
            dVdr = np.mean([dVdr00, dVdr10, dVdr01, dVdr11])
            dVdt00 = V010 - V000
            dVdt10 = V110 - V100
            dVdt01 = V011 - V001
            dVdt11 = V111 - V101
            dVdt = np.mean([dVdt00, dVdt10, dVdt01, dVdt11])
            dVdp00 = V001 - V000
            dVdp10 = V101 - V100
            dVdp01 = V011 - V010
            dVdp11 - V111 - V110
            dVdp = np.mean([dVdp00, dVdp10, dVdp01, dVdp11])
            D[i] = [dVdr, dVdt, dVdp, 1]
            res[i] = 
