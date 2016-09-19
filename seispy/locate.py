from math import radians
import mmap
import os.path
import struct
import time

import numpy as np

from seispy.core import Origin
from seispy.geometry import sph2geo

HDR_OFST = 36

class Locator(object):
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
        #r0, theta0, phi0, t0 = self._grid_search(origin)
        r0, theta0, phi0, t0 = self.nodes['r'][20, 161, 136],\
                               self.nodes['theta'][20, 161, 136],\
                               self.nodes['phi'][20, 161, 136],\
                               1357001730.69
        r0, theta0, phi0, t0, sdobs0, res0 = self._subgrid_inversion(r0, theta0, phi0, t0,\
                                                       origin.arrivals)
        lat0, lon0, z0 = sph2geo(r0, theta0, phi0)
        lon0 -= 360.
        return Origin(lat0, lon0, z0, t0)

    def _get_node_tt(self, arrival, ir, itheta, iphi):
        f = self.mmttf[arrival.sta][arrival.phase]
        iphi = iphi - 1 if iphi > 0 else 0
        itheta = itheta - 1 if itheta > 0 else 0
        offset =    ( self.grid['nr'] * self.grid['ntheta'] * iphi\
                    + self.grid['nr'] * itheta\
                    + ir)\
                * 4\
                + HDR_OFST
        f.seek(int(round(offset)))
        return struct.unpack("f", f.read(4))[0]

    def _get_tt(self, arrival, r, theta, phi):
        f = self.mmttf[arrival.sta][arrival.phase]
        nr = self.grid['nr']
        ntheta = self.grid['ntheta']
        nphi = self.grid['nphi']
        dr = self.grid['dr']
        dtheta = self.grid['dtheta']
        dphi = self.grid['dphi']
        ir0 = (r - self.nodes['r'][0, 0, 0]) / dr
        itheta0 = abs((theta - self.nodes['theta'][0, 0, 0])) / dtheta
        iphi0 = (phi - self.nodes['phi'][0, 0, 0]) / dphi
        delr, deltheta, delphi = ir0 % 1., itheta0 % 1., iphi0 % 1.
        ir0, itheta0, iphi0 = int(ir0), int(itheta0), int(iphi0)
        ir1 = ir0 if ir0 == nr - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == ntheta - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == nphi - 1 else iphi0 + 1
        V000 = self._get_node_tt(arrival, ir0, itheta0, iphi0)
        V100 = self._get_node_tt(arrival, ir1, itheta0, iphi0)
        V010 = self._get_node_tt(arrival, ir0, itheta1, iphi0)
        V110 = self._get_node_tt(arrival, ir1, itheta1, iphi0)
        V001 = self._get_node_tt(arrival, ir0, itheta0, iphi1)
        V101 = self._get_node_tt(arrival, ir1, itheta0, iphi1)
        V011 = self._get_node_tt(arrival, ir0, itheta1, iphi1)
        V111 = self._get_node_tt(arrival, ir1, itheta1, iphi1)
        V00 = V000 + (V100 - V000) * delr
        V10 = V010 + (V110 - V010) * delr
        V01 = V001 + (V101 - V001) * delr
        V11 = V011 + (V111 - V001) * delr
        V0 = V00 + (V10 - V00) * deltheta
        V1 = V01 + (V11 - V01) * deltheta
        return V0 + (V1 - V0) * delphi

    def _grid_search(self, origin):
        nr = self.grid['nr']
        ntheta = self.grid['ntheta']
        nphi = self.grid['nphi']
        best_fit = float('inf')
        for (ir, itheta, iphi)\
                in [(i, j, k) for i in range(nr)\
                              for j in range(ntheta)\
                              for k in range(nphi)]:
            at = [arr.time for arr in origin.arrivals]
            tt = [self._get_node_tt(arr, ir, itheta, iphi) for arr in arrivals]
            ots = [at[i] - tt[i] for i in range(len(at))]
            ot = np.mean(ots)
            misfit = sum([abs((ot + tt[i]) - at[i]) for i in range(len(at))])
            if misfit < best_fit:
                best_fit = misfit
                ir0, itheta0, iphi0, t0 = ir, itheta, iphi, ot
                print ir0, itheta0, iphi0, t0, best_fit
        return self.nodes['r'][ir0, itheta0, iphi0],\
               self.nodes['theta'][ir0, itheta0, iphi0],\
               self.nodes['phi'][ir0, itheta0, iphi0],\
               t0
            
    def _initialize_mmap(self, origin):
        mmttf, grid = {}, None
        for arrival in origin.arrivals:
            sta = arrival.sta
            if sta not in mmttf:
                mmttf[sta] = {}
            f = open(os.path.abspath(os.path.join(self.tt_dir, "%s.%s.tt"\
                    % (sta, arrival.phase))), 'rb')
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            mmttf[sta][arrival.phase] = mm
            if not grid:
                grid = {}
                grid['nr'], grid['nlat'], grid['nlon']\
                        = struct.unpack("3i", mm.read(12))
                grid['dr'], grid['dlat'], grid['dlon']\
                        = struct.unpack("3f", mm.read(12))
                grid['r0'], grid['lat0'], grid['lon0']\
                        = struct.unpack("3f", mm.read(12))
                grid['dtheta'] = radians(grid['dlat'])
                grid['dphi'] = radians(grid['dlon'])
                grid['ntheta'], grid['nphi'] = grid['nlat'], grid['nlon']
                grid['theta0'] = radians(90 - grid['lat0'])
                grid['phi0'] = radians(grid['lon0'])
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

    def _subgrid_inversion(self, r0, theta0, phi0, t0, arrivals):
        ir0 = (r0 - self.grid['r0']) / self.grid['dr']
        itheta0 = abs(theta0 - self.grid['theta0'])\
                / self.grid['dtheta']
        iphi0 = (phi0 - self.grid['phi0']) / self.grid['dphi']
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
            V000 = self._get_node_tt(arrival, ir0, itheta0, iphi0)
            V100 = self._get_node_tt(arrival, ir1, itheta0, iphi0)
            V010 = self._get_node_tt(arrival, ir0, itheta1, iphi0)
            V110 = self._get_node_tt(arrival, ir1, itheta1, iphi0)
            V001 = self._get_node_tt(arrival, ir0, itheta0, iphi1)
            V101 = self._get_node_tt(arrival, ir1, itheta0, iphi1)
            V011 = self._get_node_tt(arrival, ir0, itheta1, iphi1)
            V111 = self._get_node_tt(arrival, ir1, itheta1, iphi1)
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
            dVdp11 = V111 - V110
            dVdp = np.mean([dVdp00, dVdp10, dVdp01, dVdp11])
            D[i] = [dVdr, dVdt, dVdp, 1]
            res[i] = arrivals[i].time - (t0 + self._get_tt(arrivals[i], r0, theta0, phi0))
        delU, res_, rank, s = np.linalg.lstsq(D, res)
        delr, deltheta, delphi, delt = delU
        r0 += delr * self.grid['dr']
        theta0 += deltheta * self.grid['dtheta']
        phi0 += delphi * self.grid['dphi']
        t0 += delt
        res0 = np.array([arrival.time - (t0 + self._get_tt(arrival, r0, theta0, phi0))\
                for arrival in arrivals])
        sdobs0 = np.std(res0)
        return r0, theta0, phi0, t0, sdobs0, res0

if __name__ == "__main__":
    from seispy.core import Arrival, Origin
    origin = Origin(33.9723, -116.8177, 16.5905, 1357001730.24105)
    arrivals = [Arrival('SNO', 1357001733.41840, 'P', 0.25),
                Arrival('MSC', 1357001734.31840, 'P', 0.25),
                Arrival('FOST', 1357001735.49500, 'P', 0.25),
                Arrival('SNO', 1357001735.59840, 'S', 0.25),
                Arrival('IWR', 1357001735.76950, 'P', 0.25),
                Arrival('GVAR1', 1357001736.87450, 'P', 0.25),
                Arrival('BCCC', 1357001737.15490, 'P', 0.25),
                Arrival('MSC', 1357001737.29840, 'S', 0.25),
                Arrival('SFTR', 1357001737.34500, 'P', 0.25),
                Arrival('DGR', 1357001737.68840, 'P', 0.25),
                Arrival('FOST', 1357001739.24500, 'S', 0.25),
                Arrival('IWR', 1357001739.56950, 'S', 0.25),
                Arrival('TFRD', 1357001740.40950, 'P', 0.25),
                Arrival('FRD', 1357001740.41840, 'P', 0.25),
                Arrival('GVAR1', 1357001741.83950, 'S', 0.25),
                Arrival('DGR', 1357001742.65840, 'S', 0.25),
                Arrival('BCCC', 1357001742.67490, 'S', 0.25),
                Arrival('TFRD', 1357001747.72950, 'S', 0.25),
                Arrival('FRD', 1357001747.74840, 'S', 0.25),
                Arrival('SFTR', 1357001743.89000, 'S', 0.25)]
    origin.add_arrivals(arrivals)
    locator = Locator("/home/shake/malcolcw/data/fm3d_ttimes")
    print locator.relocate(origin)
