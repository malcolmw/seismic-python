from math import radians, degrees
import mmap
import os.path
import struct
import time

import numpy as np

from seispy.core import Origin
from seispy.geometry import EARTH_RADIUS,\
                            sph2geo

HDR_OFST = 36

class Locator(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def _locate_init(self, origin):
        self.mmttf, self.grid = self._initialize_mmap(origin)
        grid = self.grid
        arrivals = [arrival for arrival in origin.arrivals\
                            if arrival.station in self.mmttf]
        if not self.check_nsta(arrivals):
            print "unable to relocate event, not enough stations"
            return None
        origin.clear_arrivals()
        origin.add_arrivals(arrivals)
        r = [grid['r0'] + grid['dr'] * ir for ir in range(grid['nr'])]
        theta = [radians(90. - grid['lat0'] - grid['dlat'] * ilat)\
                for ilat in range(grid['nlat'])]
        phi = [radians((grid['lon0'] + grid['dlon'] * ilon) % 360.)\
                for ilon in range(grid['nlon'])]
        R, T, P = np.meshgrid(r, theta, phi, indexing='ij')
        self.nodes = {'r': R, 'theta': T, 'phi': P}
        self.byteoffset = np.ndarray(shape=self.nodes['r'].shape)
        offset = 36
        for iphi in range(self.grid['nphi']):
            for itheta in range(self.grid['ntheta']):
                for ir in range(self.grid['nr']):
                    self.byteoffset[ir, itheta, iphi] = offset
                    offset += 4
        return True

    def check_nsta(self, arrivals):
        stations = []
        for arrival in arrivals:
            if arrival.station not in stations:
                stations += [arrival.station]
        if len(stations) >= self.cfg['min_nsta']:
            return True
        else:
            return False

    def locate(self, origin):
        if not self._locate_init(origin):
            return None
        r0, theta0, phi0, t0 = self._grid_search(origin)
        soln = self._subgrid_inversion(r0, theta0, phi0, t0, origin.arrivals)
        if soln ==  None:
            return None
        else:
            r0, theta0, phi0, t0, sdobs0, res0, arrivals = soln
        lat0, lon0, z0 = sph2geo(r0, theta0, phi0)
        #lon0 -= 360.
        return Origin(lat0, lon0, z0, t0,
                      arrivals=arrivals,
                      evid=origin.evid,
                      sdobs=sdobs0)

    def relocate(self, origin):
        if not self._locate_init(origin):
            return None
        grid = self.grid
        if not (EARTH_RADIUS - grid['mr'] < origin.depth < EARTH_RADIUS - grid['r0'])\
                or not (grid['lat0'] < origin.lat < grid['mlat'])\
                or not (grid['lon0'] < origin.lon < grid['mlon']):
            #print "unable to use starting location outside of grid, performing grid search"
            print "unable to locate, starting location outside of grid"
            return None
            return self.locate(origin)
        r0 = EARTH_RADIUS - origin.depth
        theta0 = radians(90 - origin.lat)
        phi0 = radians(origin.lon % 360.)
        t0 = float(origin.time)
        soln = self._subgrid_inversion(r0, theta0, phi0, t0, origin.arrivals)
        if soln ==  None:
            return None
        else:
            r0, theta0, phi0, t0, sdobs0, res0, arrivals = soln
        lat0, lon0, z0 = sph2geo(r0, theta0, phi0)
        #lon0 -= 360.
        return Origin(lat0, lon0, z0, t0,
                      arrivals=arrivals,
                      evid=origin.evid,
                      sdobs=sdobs0)

    def _get_node_tt(self, arrival, ir, itheta, iphi):
        f = self.mmttf[arrival.station][arrival.phase]
        offset = self.byteoffset[ir, itheta, iphi]
        f.seek(int(offset))
        return struct.unpack("f", f.read(4))[0]

    def _get_tt(self, arrival, r, theta, phi):
        f = self.mmttf[arrival.station][arrival.phase]
        nr = self.grid['nr']
        ntheta = self.grid['ntheta']
        nphi = self.grid['nphi']
        dr = self.grid['dr']
        dtheta = self.grid['dtheta']
        dphi = self.grid['dphi']
        ir0 = (r - self.grid['r0']) / dr
        itheta0 = (self.grid['theta0'] - theta) / dtheta
        iphi0 = (phi - self.grid['phi0']) / dphi
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
        print "grid searching for", origin
        nr = self.grid['nr']
        ntheta = self.grid['ntheta']
        nphi = self.grid['nphi']
        best_fit = float('inf')
        for (ir, itheta, iphi)\
                in [(i, j, k) for i in range(nr)\
                              for j in range(ntheta)\
                              for k in range(nphi)]:
            at = [float(arr.time) for arr in origin.arrivals]
            tt = [self._get_node_tt(arr, ir, itheta, iphi) for arr in origin.arrivals]
            ots = [float(at[i] - tt[i]) for i in range(len(at))]
            ot = np.mean(ots)
            misfit = sum([abs((ot + tt[i]) - at[i]) for i in range(len(at))])
            if misfit < best_fit:
                best_fit = misfit
                ir0, itheta0, iphi0, t0 = ir, itheta, iphi, ot
        return self.nodes['r'][ir0, itheta0, iphi0],\
               self.nodes['theta'][ir0, itheta0, iphi0],\
               self.nodes['phi'][ir0, itheta0, iphi0],\
               t0
            
    def _initialize_mmap(self, origin):
        mmttf, grid = {}, None
        for arrival in origin.arrivals:
            sta = arrival.station
            try:
                f = open(os.path.abspath(os.path.join(self.cfg['tt_dir'], "%s.%s.tt"\
                        % (sta, arrival.phase))), 'rb')
            except IOError:
                print "no %s-wave travel-time file for %s" % (arrival.phase, sta)
                continue
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            if sta not in mmttf:
                mmttf[sta] = {}
            mmttf[sta][arrival.phase] = mm
            if not grid:
                grid = {}
                grid['nr'], grid['nlat'], grid['nlon']\
                        = struct.unpack("3i", mm.read(12))
                grid['dr'], grid['dlat'], grid['dlon']\
                        = struct.unpack("3f", mm.read(12))
                grid['r0'], grid['lat0'], grid['lon0']\
                        = struct.unpack("3f", mm.read(12))
                grid['mr'] = grid['r0'] + (grid['nr'] - 1) * grid['dr']
                grid['mlat'] = grid['lat0'] + (grid['nlat'] - 1) * grid['dlat']
                grid['mlon'] = grid['lon0'] + (grid['nlon'] - 1) * grid['dlon']
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

    def _subgrid_inversion(self, r0, theta0, phi0, t0, arrivals, itern=0):
        res_start = np.array([float(arrival.time)\
                              - (t0 + self._get_tt(arrival, r0, theta0, phi0))\
                              for arrival in arrivals])
        sdobs_start = np.sqrt(np.sum(np.square(res_start))) / (len(res_start) - 4)
        ir0 = (r0 - self.grid['r0']) / self.grid['dr']
        itheta0 = (self.grid['theta0'] - theta0)\
                / self.grid['dtheta']
        iphi0 = (phi0 - self.grid['phi0']) / self.grid['dphi']
        delr = ir0 % 1
        deltheta = itheta0 % 1
        delphi = iphi0 % 1
        ir0, itheta0, iphi0 = int(ir0), int(itheta0), int(iphi0)
        ir1 = ir0 if ir0 == self.grid['nr'] - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == self.grid['ntheta'] - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == self.grid['nphi'] - 1 else iphi0 + 1
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
            res[i] = float(arrival.time) - (t0 + self._get_tt(arrival, r0, theta0, phi0))
        delU, res_, rank, s = np.linalg.lstsq(D, res)
        delr, deltheta, delphi, delt = delU
        r0 += delr * self.grid['dr']
        theta0 += deltheta * self.grid['dtheta']
        phi0 += delphi * self.grid['dphi']
        t0 += delt
        #if solution does not converge within grid, return None
        gr0, gtheta0, gphi0 = self.grid['r0'], self.grid['theta0'], self.grid['phi0']
        gnr, gntheta, gnphi = self.grid['nr'], self.grid['ntheta'], self.grid['nphi']
        gdr, gdtheta, gdphi = self.grid['dr'], self.grid['dtheta'], self.grid['dphi']
        #if solution is above propagation grid, fix depth to surface
        #if r0 > gr0 + gdr * (gnr - 1):
        #    r0 = gr0 + gdr * (gnr - 1)
        #    #fix_depth = True
        if not gr0 < r0 < gr0 + gdr * (gnr - 1)\
                or not (gtheta0 - (gntheta - 1) * gdtheta < theta0 < gtheta0)\
                or not (gphi0 < phi0 < gphi0 + (gnphi - 1) * gdphi):
            return None
        res0 = np.array([float(arrival.time) - (t0 + self._get_tt(arrival, r0, theta0, phi0))\
                for arrival in arrivals])
        sdobs0 = np.sqrt(np.sum(np.square(res0))) / (len(res0) - 4)
        arrivals = self.remove_outliers(r0, theta0, phi0, t0, arrivals)
        if not self.check_nsta(arrivals):
            print "not enough stations remaining"
            return None
        if itern < self.cfg['max_iterations'] and\
                abs(sdobs0 - sdobs_start) > self.cfg['convergance_threshold']:
            self._subgrid_inversion(r0, theta0, phi0, t0,
                                    arrivals,
                                    itern=itern + 1)
        elif itern >= self.cfg['max_iterations']:
            print "soultion did not converge after %d iterations" % itern
            return None
        return r0, theta0, phi0, t0, sdobs0, res0, arrivals

    def remove_outliers(self, r0, theta0, phi0, t0, arrivals):
        res = np.array([float(arr.time) - (t0 + self._get_tt(arr, r0, theta0, phi0))\
                    for arr in arrivals])
        new_arrivals = []
        for i in range(len(arrivals)):
            arr = arrivals[i]
            r = res[i]
            tol = self.cfg['P_residual_tolerance']\
                  if  arr.phase == 'P'\
                  else self.cfg['S_residual_tolerance']
            if abs(r) < tol: new_arrivals += [arr]
        print "removing %d/%d arrivals"\
                % ((len(arrivals) - len(new_arrivals)), len(arrivals))
        return new_arrivals

