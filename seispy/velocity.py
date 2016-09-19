from math import cos,\
                 degrees,\
                 pi,\
                 radians,\
                 sin
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata

import numpy as np
from numpy import linspace,\
                  meshgrid,\
                  ndarray,\
                  zeros
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator, Rbf
from scipy import ndimage
#from geometry import EARTH_RADIUS,\
from seispy.geoid import Geoid
from seispy.geometry import EARTH_RADIUS,\
                            geo2sph,\
                            sph2geo,\
                            sph2xyz,\
                            Vector


class VelocityModel(object):
    """
    This class is intended to facilitate querying and plotting of velocity models.

    For now, assume a model defined on a regular grid in spherical coordinates.

    .. todo::
       document this class.
    """
    def __init__(self, infile, topo=None, fmt='fang'):
        if fmt.upper() == 'FANG':
            self._read_fang(infile, topo)

    def _read_fang(self, infile, topo_infile):
        #initialize a Geoid object with topography
        self.geoid = Geoid(topo_infile)
        #Read grid nodes.
        infile = open(infile)
        phi_nodes = [radians(float(lon) % 360.) for lon in infile.readline().split()]
        theta_nodes = [radians(90. - float(lat)) for lat in infile.readline().split()]
        r_nodes = [EARTH_RADIUS - float(z) for z in infile.readline().split()]
        R, T, P = np.meshgrid(r_nodes, theta_nodes, phi_nodes, indexing='ij')
        self.nodes = {'r': R, 'theta': T, 'phi': P}
        self.nodes['nr'] = R.shape[0]
        self.nodes['r_min'] = min(r_nodes)
        self.nodes['r_max'] = max(r_nodes)
        self.nodes['dr'] = (self.nodes['r_max'] - self.nodes['r_min']) / (self.nodes['nr'] - 1)
        self.nodes['ntheta'] = T.shape[1]
        self.nodes['theta_min'] = min(theta_nodes)
        self.nodes['theta_max'] = max(theta_nodes)
        self.nodes['dtheta'] = (self.nodes['theta_max'] - self.nodes['theta_min']) / (self.nodes['ntheta'] - 1)
        self.nodes['nphi'] = P.shape[2]
        self.nodes['phi_min'] = min(phi_nodes)
        self.nodes['phi_max'] = max(phi_nodes)
        self.nodes['dphi'] = (self.nodes['phi_max'] - self.nodes['phi_min']) / (self.nodes['nphi'] - 1)
        #print self.nodes['nr'], self.nodes['r_min'], self.nodes['r_max'], self.nodes['dr']
        #print self.nodes['ntheta'], self.nodes['theta_min'], self.nodes['theta_max'], self.nodes['dtheta']
        #print self.nodes['nphi'], self.nodes['phi_min'], self.nodes['phi_max'], self.nodes['dphi']
        #exit()
        self.values = {'Vp': np.empty(shape=(len(r_nodes), len(theta_nodes), len(phi_nodes))),
                       'Vs': np.empty(shape=(len(r_nodes), len(theta_nodes), len(phi_nodes)))}
        for phase in ('Vp', 'Vs'):
            for ir in range(len(r_nodes)):
                for itheta in range(len(theta_nodes)):
                    line = infile.readline().split()
                    for iphi in range(len(line)):
                        #values[phase] += [float(line[iphi])]
                        self.values[phase][ir, itheta, iphi] = float(line[iphi])
        #flip r and theta axis so they increase with increasing index
        self.nodes['r'] = self.nodes['r'][::-1]
        self.nodes['theta'] = self.nodes['theta'][:,::-1]
        for phase in ('Vp', 'Vs'):
            self.values[phase] = self.values[phase][::-1]
            self.values[phase] = self.values[phase][:,::-1]
        self._basement = {'Vp': np.median(np.concatenate(self.values['Vp'][0])),
                          'Vs': np.median(np.concatenate(self.values['Vs'][0]))}
        self._default = {'Vp': np.median(np.concatenate(np.concatenate(self.values['Vp']))),
                         'Vs': np.median(np.concatenate(np.concatenate(self.values['Vs'])))}
        #self._air = {'Vp': 0.3432,
        self._air = {'Vp': 1.0,
                     'Vs': 1.0}

    def _get_V_trilinear_interpolation(self, r, theta, phi, phase):
        #Make sure phi is a postive number < 2 * pi.
        phi %= (2 * pi)
        #If the position requested is above the surface, return the
        #velocity of air for Vp and a NULL value, -1, for Vs.
        if r > self.geoid(phi, theta, coords="spherical"):
            return self._air[phase]
        #If the location requested is below the grid, return the
        #basement velocity.
        if r < self.nodes['r_min']:
            return self._basement[phase]
        #If the location requested is outside the grid laterally,
        if not (self.nodes['theta_min'] <= theta <= self.nodes['theta_max'])\
                or not (self.nodes['phi_min'] <= phi <= self.nodes['phi_max']):
            return self._default[phase]
        ir0 = (r - self.nodes['r_min']) / self.nodes['dr']
        delta_r = ir0 % 1
        ir0 = int(ir0)
        itheta0 = (theta - self.nodes['theta_min']) / self.nodes['dtheta']
        delta_theta = itheta0 % 1
        itheta0 = int(itheta0)
        iphi0 = (phi - self.nodes['phi_min']) / self.nodes['dphi']
        delta_phi = iphi0 % 1
        iphi0 = int(iphi0)
        ir1 = ir0 if ir0 == self.nodes['nr'] - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == self.nodes['ntheta'] - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == self.nodes['nphi'] - 1 else iphi0 + 1
        values = self.values[phase]
        V000, V100 = values[ir0, itheta0, iphi0], values[ir1, itheta0, iphi0]
        V010, V110 = values[ir0, itheta1, iphi0], values[ir1, itheta1, iphi0]
        V001, V101 = values[ir0, itheta0, iphi1], values[ir1, itheta0, iphi1]
        V011, V111 = values[ir0, itheta1, iphi1], values[ir1, itheta1, iphi1]
        V00 = V000 + (V100 - V000) * delta_r
        V10 = V010 + (V110 - V010) * delta_r
        V01 = V001 + (V101 - V001) * delta_r
        V11 = V011 + (V111 - V011) * delta_r
        V0 = V00 + (V10 - V00) * delta_theta
        V1 = V01 + (V11 - V01) * delta_theta
        return V0 + (V1 - V0) * delta_phi

    def _get_V_spline_interpolation(self, r, theta, phi, phase):
        #Make sure phi is a postive number < 2 * pi.
        phi %= (2 * pi)
        ir = (r - self.nodes['r_min']) / self.nodes['dr']
        itheta = (theta - self.nodes['theta_min']) / self.nodes['dtheta']
        iphi = (phi - self.nodes['phi_min']) / self.nodes['dphi']
        #If the position requested is above the surface, return the
        #velocity of air for Vp and a NULL value, -1, for Vs.
        if r > self.geoid(phi, theta, coords="spherical"):
            return self._air[phase]
        #If the location requested is below the grid, return the
        #basement velocity.
        if r < self.nodes['r_min']:
            return self._basement[phase]
        #If the location requested is outside the grid laterally,
        #return the default velocity.
        if not (self.nodes['theta_min'] <= theta <= self.nodes['theta_max'])\
                or not (self.nodes['phi_min'] <= phi <= self.nodes['phi_max']):
            return self._default[phase]
        return ndimage.map_coordinates(self.values[phase], [[ir], [itheta], [iphi]], order=4)[0]
        #return float(self._interpolator[phase](r, theta, phi))

    def get_Vp(self, lat, lon, depth, interpolation_method='linear'):
        r, theta, phi = geo2sph(lat, lon, depth)
        if interpolation_method == 'linear':
            return self._get_V_trilinear_interpolation(r, theta, phi, 'Vp')
        elif interpolation_method == 'spline':
            return self._get_V_spline_interpolation(r, theta, phi, 'Vp')

    def get_Vs(self, lat, lon, depth, interpolation_method='linear'):
        r, theta, phi = geo2sph(lat, lon, depth)
        if interpolation_method == 'linear':
            return self._get_V_trilinear_interpolation(r, theta, phi, 'Vs')
        elif interpolation_method == 'spline':
            return self._get_V_spline_interpolation(r, theta, phi, 'Vs')

    def _plot(self, lat, lon, depth, phase, nx, ny):
        lon %= 360.
        X, Y, V = [], [], []
        phim = np.mean([self.nodes['phi_max'], self.nodes['phi_min']])
        thetam = np.mean([self.nodes['theta_max'], self.nodes['theta_min']])
        if lat == -999 and lon == -999:
            title = "Depth horizon - %.1f [km]" % depth
            xlabel = "Distance from %.2f [km]" % degrees(phim)
            ylabel = "Distance from %.2f [km]" % (90 - degrees(thetam))
            r = EARTH_RADIUS - depth
            theta_nodes = linspace(self.nodes['theta_min'],
                                   self.nodes['theta_max'],
                                   ny)
            phi_nodes = linspace(self.nodes['phi_min'],
                                   self.nodes['phi_max'],
                                   nx)
            X, Y = meshgrid(phi_nodes, theta_nodes, indexing='ij')
            V = np.ndarray(shape=X.shape)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    phi = X[i, j]
                    theta = Y[i, j]
                    V[i, j] = self._get_V(r, Y[i, j], X[i, j], phase)
                    X[i, j] = r * cos(pi / 2 - (phi - phim))
                    Y[i, j] = r * sin(theta - thetam)
        elif lat == -999 and depth == -999:
            title = "Vertical, longitudinal slice %.2f" % lon
            xlabel = "Distance from %.2f [km]" % (90 - degrees(thetam))
            ylabel = "Depth from surface [km]"
            phi = radians(lon)
            r_nodes = linspace(self.nodes['r_min'],
                               self.nodes['r_max'],
                               ny)
            theta_nodes = linspace(self.nodes['theta_min'],
                                   self.nodes['theta_max'],
                                   nx)
            X, Y = np.meshgrid(theta_nodes, r_nodes, indexing='ij')
            V = np.ndarray(shape=X.shape)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    r = Y[i, j]
                    theta = X[i, j]
                    V[i, j] = self._get_V(r, theta, phi, phase)
                    X[i, j] = r * sin(theta - thetam)
                    Y[i, j] = r * cos(theta - thetam) - EARTH_RADIUS
        elif lon == -999 and depth == -999:
            title = "Vertical, latitudinal slice %.2f" % lat
            xlabel = "Distance from %.2f [km]" % degrees(phim)
            ylabel = "Depth from surface [km]"
            theta = radians(90 - lat)
            r_nodes = linspace(self.nodes['r_min'],
                               self.nodes['r_max'],
                               ny)
            phi_nodes = linspace(self.nodes['phi_min'],
                                 self.nodes['phi_max'],
                                 nx)
            X, Y = np.meshgrid(phi_nodes, r_nodes, indexing='ij')
            V = np.ndarray(shape=X.shape)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    V[i, j] = self._get_V(Y[i, j], theta, X[i, j], phase)
                    phi, r = X[i, j], Y[i, j]
                    X[i, j] = r * cos(pi / 2 - (phi - phim))
                    Y[i, j] = r * sin(pi / 2 - (phi - phim)) - EARTH_RADIUS
        Vair = self._air[phase]
        V = np.ma.masked_inside(V, Vair - 0.1 * Vair, Vair + 0.1 * Vair)
        fig = plt.figure()
        fig.suptitle(title)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel(xlabel)
        ax.set_xlim(min([min(x) for x in X]),
                    max([max(x) for x in X]))
        ax.set_ylabel(ylabel)
        ax.set_ylim(min([min(y) for y in Y]),
                    max([max(y) for y in Y]))
        im = ax.pcolormesh(X, Y, V,
                           cmap=plt.get_cmap('hsv'))
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("%s [km/s]" % phase)
        plt.show()

    def write_fm3d(self, propgrid, stretch=1.01, size_ratio=2, basement=30.):
        self.write_propgrid(propgrid)
        self.write_vgrids(propgrid,
                          stretch=stretch,
                          size_ratio=size_ratio)
        self.write_interfaces(propgrid, 
                              stretch=stretch,
                              size_ratio=size_ratio,
                              basement=basement)

    def write_vgrids(self, grid, stretch=1.01, size_ratio=2):
        stretch = 1.01
        size_ratio = 2
        outfileP = open("vgrids.in_P", "w")
        outfileS = open("vgrids.in_S", "w")
        outfileP.write("1 1\n")
        outfileS.write("1 1\n")
        pnr, pnlat, pnlon =  grid['nr'], grid['nlat'], grid['nlon']
        pdr, pdlat, pdlon = grid['dr'], radians(grid['dlat']), radians(grid['dlon'])
        ph0, plat0, plon0 = grid['h0'], radians(grid['lat0']), radians(grid['lon0'] % 360.)
        pr0 = EARTH_RADIUS + ph0 - ((pnr - 1) * pdr)
        i = (pnr - 1) % size_ratio
        pnr = pnr + (size_ratio - i) if i > 0 else pnr
        i = (pnlat - 1) % size_ratio
        pnlat = pnlat + (size_ratio - i) if i > 0 else pnlat
        i = (pnlon - 1) % size_ratio
        pnlon = pnlon + (size_ratio - i) if i > 0 else pnlon
        nr = (pnr - 1) / size_ratio + 3
        nlat = (pnlat - 1) / size_ratio + 3
        nlon = (pnlon - 1) / size_ratio + 3
        dr = stretch * pdr * size_ratio
        dlat = stretch * pdlat * size_ratio
        dlon = stretch * pdlon * size_ratio
        r0 = pr0 - dr - (nr - 1) * dr * (stretch - 1.0) / 2
        lat0 = plat0 - dlat - (nlat - 1) * dlat * (stretch - 1.0) / 2
        lon0 = plon0 - dlon - (nlon - 1) * dlon * (stretch - 1.0) / 2
        for outfile in (outfileP, outfileS):
            outfile.write("%d %d %d\n" % (nr, nlat, nlon))
            outfile.write("%.4f %.4f %.4f\n" % (dr, dlat, dlon))
            outfile.write("%.4f %.4f %.4f\n" % (r0, lat0, lon0))
        for ir in range(nr):
            for ilat in range(nlat):
                for ilon in range(nlon):
                    lat = lat0 + dlat * ilat
                    _lat = degrees(lat)
                    lon = lon0 + dlon * ilon
                    _lon = degrees(lon) % 360.
                    r = r0 + dr * ir
                    depth = EARTH_RADIUS - r
                    outfileP.write("%f\n" % self.get_Vp(_lat, _lon, depth))
                    outfileS.write("%f\n" % self.get_Vs(_lat, _lon, depth))
        outfileP.close()
        outfileS.close()

    def write_interfaces(self, grid, stretch=1.01, size_ratio=2, basement=30.):
        outfile = open("interfaces.in", "w")
        pnlat, pnlon =  grid['nlat'], grid['nlon']
        pdlat, pdlon = radians(grid['dlat']), radians(grid['dlon'])
        plat0, plon0 = radians(grid['lat0']), radians(grid['lon0'] % 360.)
        i = (pnlat - 1) % size_ratio
        pnlat = pnlat + (size_ratio - i) if i > 0 else pnlat
        i = (pnlon - 1) % size_ratio
        pnlon = pnlon + (size_ratio - i) if i > 0 else pnlon
        nlat = (pnlat - 1) / size_ratio + 3
        nlon = (pnlon - 1) / size_ratio + 3
        dlat = stretch * pdlat * size_ratio
        dlon = stretch * pdlon * size_ratio
        lat0 = plat0 - dlat - (nlat - 1) * dlat * (stretch - 1.0) / 2
        lon0 = plon0 - dlon - (nlon - 1) * dlon * (stretch - 1.0) / 2
        outfile.write("2\n")
        outfile.write("%d %d\n" % (nlat, nlon))
        outfile.write("%.4f %.4f\n" % (dlat, dlon))
        outfile.write("%.4f %.4f\n" % (lat0, lon0))
        for interface in ('top', 'bottom'):
            if interface == 'top':
                R = lambda lat, lon: EARTH_RADIUS + 5.
            elif interface == 'bottom':
                R = lambda lat, lon: EARTH_RADIUS - basement
            for ilat in range(nlat):
                lat = lat0 + ilat * dlat
                _lat = degrees(lat)
                for ilon in range(nlon):
                    lon = lon0 + ilon * dlon
                    _lon = degrees(lon)
                    _lon %= 360.
                    outfile.write("%.4f\n" % R(_lat, _lon))
        outfile.close()

    def write_propgrid(self, pgrid):
        nr, nlon, nlat = pgrid['nr'], pgrid['nlon'], pgrid['nlat']
        h0, lon0, lat0 = pgrid['h0'], pgrid['lon0'], pgrid['lat0']
        dr, dlon, dlat = pgrid['dr'], pgrid['dlon'], pgrid['dlat']
        outfile = open("propgrid.in", "w")
        outfile.write("%d %d %d\n" % (nr, nlat, nlon))
        outfile.write("%.6f %.6f %.6f\n" % (dr, dlat, dlon))
        outfile.write("%.6f %.6f %.6f\n" % (h0, lat0, lon0))
        outfile.write("5 10")
        outfile.close()

    def plot_Vp(self, lat=-999, lon=-999, depth=-999, nx=50, ny=50):
        self._plot(lat, lon, depth, 'Vp', nx, ny)

    def plot_Vs(self, lat=-999, lon=-999, depth=-999, nx=50, ny=50):
        self._plot(lat, lon, depth, 'Vs', nx, ny)

    def plot_VpVs_ratio(self):
        pass

if __name__ == "__main__":
    vm = VelocityModel("/home/shake/malcolcw/products/velocity/FANG2016/original/VpVs.dat",
                       topo="/home/shake/malcolcw/data/mapping/ANZA/anza.xyz")
    vm.plot_Vp(lon=-116.455, nx=250, ny=250)
