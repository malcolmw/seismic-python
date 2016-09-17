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
from scipy.interpolate import LinearNDInterpolator
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
        lon_nodes = [float(lon) % 360 for lon in infile.readline().split()]
        lat_nodes = [float(lat) for lat in infile.readline().split()]
        z_nodes = [float(z) for z in infile.readline().split()]
        r_nodes = [EARTH_RADIUS - z for z in z_nodes]
        theta_nodes = [radians(90. - lat) for lat in lat_nodes]
        phi_nodes = [radians(lon) for lon in lon_nodes]
        nodes = [(r, t, p) for r in r_nodes\
                           for t in theta_nodes\
                           for p in phi_nodes]
        self.r_min = min(r_nodes)
        self.r_max = max(r_nodes)
        self.theta_min = min(theta_nodes)
        self.theta_max = max(theta_nodes)
        self.phi_min = min(phi_nodes)
        self.phi_max = max(phi_nodes)
        values = {'Vp': [], 'Vs': []}
        for phase in ('Vp', 'Vs'):
            for ir in range(len(r_nodes)):
                for itheta in range(len(theta_nodes)):
                    line = infile.readline().split()
                    for iphi in range(len(line)):
                        values[phase] += [float(line[iphi])]
        self._interpolator = {'Vp': LinearNDInterpolator(nodes, values['Vp']),
                              'Vs': LinearNDInterpolator(nodes, values['Vs'])}
        self._basement = {'Vp': np.median([values['Vp'][i]\
                                            for i in range(len(values['Vp']))\
                                            if nodes[i][0] == self.r_min]),
                          'Vs': np.median([values['Vs'][i]\
                                            for i in range(len(values['Vs']))\
                                            if nodes[i][0] == self.r_min])}
        self._default = {'Vp': np.median(values['Vp']),
                         'Vs': np.median(values['Vs'])}
        self._air = {'Vp': 0.3432,
                     'Vs': 0.1}

    def _get_V(self, r, theta, phi, phase):
        #Make sure phi is a postive number < 2 * pi.
        phi %= (2 * pi)
        #If the position requested is above the surface, return the
        #velocity of air for Vp and a NULL value, -1, for Vs.
        if r > self.geoid(phi, theta, coords="spherical"):
            return self._air[phase]
        #If the location requested is below the grid, return the
        #basement velocity.
        if r < self.r_min:
            return self._basement[phase]
        #If the location requested is outside the grid laterally,
        #return the default velocity.
        if not (self.theta_min <= theta <= self.theta_max)\
                or not (self.phi_min <= phi <= self.phi_max):
            return self._default[phase]
        return self._interpolator[phase]((r, theta, phi))

    def get_Vp(self, lat, lon, depth):
        r, theta, phi = geo2sph(lat, lon, depth)
        return self._get_V(r, theta, phi, 'Vp')

    def get_Vs(self, lat, lon, depth):
        r, theta, phi = geo2sph(lat, lon, depth)
        return self._get_V(r, theta, phi, 'Vs')

    def _plot(self, lat, lon, depth, phase, nx, ny):
        X, Y, V = [], [], []
        phim = np.mean([self.phi_max, self.phi_min])
        thetam = np.mean([self.theta_max, self.theta_min])
        if lat == -999 and lon == -999:
            title = "Depth horizon - %.1f [km]" % depth
            xlabel = "Distance from %.2f [km]" % degrees(phim)
            ylabel = "Distance from %.2f [km]" % (90 - degrees(thetam))
            r = EARTH_RADIUS - depth
            theta_nodes = linspace(self.theta_min,
                                   self.theta_max,
                                   ny)
            phi_nodes = linspace(self.phi_min,
                                   self.phi_max,
                                   nx)
            X, Y = meshgrid(phi_nodes, theta_nodes)
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
            r_nodes = linspace(self.r_min,
                               self.r_max,
                               ny)
            theta_nodes = linspace(self.theta_min,
                                   self.theta_max,
                                   nx)
            X, Y = np.meshgrid(theta_nodes, r_nodes)
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
            r_nodes = linspace(self.r_min,
                               self.r_max,
                               ny)
            phi_nodes = linspace(self.phi_min,
                                 self.phi_max,
                                 nx)
            X, Y = np.meshgrid(phi_nodes, r_nodes)
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

    def write_fm3d(self, grid1, grid2, interface_grid, propgrid):
        self.write_vgrids(grid1, grid2)
        self.write_interfaces(interface_grid)
        self.write_propgrid(propgrid, grid1)

    def write_vgrids(self, grid1, grid2):
        outfileP = open("vgrids.in_P", "w")
        outfileS = open("vgrids.in_S", "w")
        outfileP.write("2 1\n")
        outfileS.write("2 1\n")
        for grid in (grid1, grid2):
            lon0, dlon, nlon = grid['lon0'], grid['dlon'], grid['nlon']
            lat0, dlat, nlat = grid['lat0'], grid['dlat'], grid['nlat']
            r0, dr, nr = grid1['r0'], grid1['dr'], grid1['nr']
            lon0, dlon, nlon = radians(lon0), radians(dlon), nlon
            lat0, dlat, nlat = radians(lat0), radians(dlat), nlat
            for outfile in (outfileP, outfileS):
                outfile.write("%d %d %d\n" % (grid['nr'], grid['nlat'], grid['nlon']))
                outfile.write("%.4f %.4f %.4f\n" % (dr, dlat, dlon))
                outfile.write("%.4f %.4f %.4f\n" % (r0, lat0, lon0))
            for ir in range(nr):
                for ilat in range(nlat):
                    for ilon in range(nlon):
                        lat = lat0 + dlat * ilat
                        _lat = degrees(lat)
                        lon = lon0 + dlon * ilon
                        _lon = degrees(lon)
                        _lon -= 360.
                        r = r0 + dr * ir
                        depth = EARTH_RADIUS - r
                        outfileP.write("%f\n" % self.get_Vp(_lat, _lon, depth))
                        outfileS.write("%f\n" % self.get_Vs(_lat, _lon, depth))
        outfileP.close()
        outfileS.close()

    def write_interfaces(self, grid):
        outfile = open("interfaces.in", "w")
        lon0, dlon, nlon = grid['lon0'], grid['dlon'], grid['nlon']
        lat0, dlat, nlat = grid['lat0'], grid['dlat'], grid['nlat']
        lon0, dlon, nlon = radians(lon0), radians(dlon), nlon
        lat0, dlat, nlat = radians(lat0), radians(dlat), nlat
        outfile.write("3\n")
        outfile.write("%d %d\n" % (nlat, nlon))
        outfile.write("%.4f %.4f\n" % (dlat, dlon))
        outfile.write("%.4f %.4f\n" % (lat0, lon0))
        for interface in ('top', 'surface', 'bottom'):
            if interface == 'top':
                R = lambda lat, lon: EARTH_RADIUS + 5.
            elif interface == 'surface':
                R = lambda lat, lon: self.geoid(lon, lat)
            elif interface == 'bottom':
                R = lambda lat, lon: EARTH_RADIUS - 29.
            for ilat in range(nlat):
                lat = lat0 + ilat * dlat
                _lat = degrees(lat)
                for ilon in range(nlon):
                    lon = lon0 + ilon * dlon
                    _lon = degrees(lon)
                    _lon -= 360.
                    outfile.write("%.4f\n" % R(_lat, _lon))
        outfile.close()

    def write_propgrid(self, propgrid, vgrid):
        nr, nlon, nlat = propgrid['nr'], propgrid['nlon'], propgrid['nlat']
        h0 = vgrid['r0'] + (vgrid['nr'] - 2.01) * vgrid['dr'] - EARTH_RADIUS
        lon0 = vgrid['lon0'] + 1.01 * vgrid['dlon']
        lat0 = vgrid['lat0'] + 1.01 * vgrid['dlat']
        hm = vgrid['r0'] + 1.01 * vgrid['dr'] - EARTH_RADIUS
        lonm = vgrid['lon0'] + (vgrid['nlon'] - 2.01) * vgrid['dlon']
        latm = vgrid['lat0'] + (vgrid['nlat'] - 2.01) * vgrid['dlat']
        dr = abs(h0 - hm) / (nr - 1)
        dlon = (lonm - lon0) / (nlon - 1)
        dlat = (latm - lat0) / (nlat - 1)
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
    for i in range(10):
        vm.plot_Vs(lat=(33 + 0.1 * i), nx=75, ny=75)
        exit()
