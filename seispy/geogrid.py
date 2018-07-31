# coding=utf-8

import numpy as np
import seispy

class GeoGrid2D(object):
    def __init__(self, lat0, lon0, nlat, nlon, dlat, dlon):
# NOTE: Origin of spherical coordinate system and geographic coordinate
# system is not the same!
# Geographic coordinate system
        self.lat0, self.lon0, _ = seispy.coords.as_geographic([lat0, lon0, 0])
        self.nlat, self.nlon = nlat, nlon
        self.dlat, self.dlon = dlat, dlon
# Spherical/Pseudospherical coordinate systems
        self.ntheta = self.nlambda = self.nlat
        self.nphi = self.nlon

        self.dtheta = self.dlambda = np.radians(self.dlat)
        self.dphi = np.radians(self.dlon)

        self.lambda0 = np.radians(self.lat0)
        self.theta0 = np.pi/2 - (self.lambda0 + (self.nlambda - 1) * self.dlambda)
        self.phi0 = np.radians(self.lon0)

    def __str__(self):
        s = "lat0, lon0: {:.15g}, {:.15g}\n".format(self.lat0,
                                                    self.lon0)
        s += "nlat, nlon: {:8d}, {:8d}\n".format(self.nlat,
                                                 self.nlon)
        s += "dlat, dlon: {:.15g}, {:.15g}\n".format(self.dlat,
                                                     self.dlon)
        s += "theta0, lambda0, phi0: {:.15g}, {:.15g}, {:.15g}\n".format(self.theta0,
                                                             self.lambda0,
                                                             self.phi0)
        s += "ntheta, nlambda, nphi : {:8d}, {:8d}\n".format(self.ntheta,
                                                  self.nlambda,
                                                  self.nphi)
        s += "dtheta, dlambda, dphi : {:.15g}, {:.15g}, {:.15g}".format(self.dtheta,
                                                             self.dlambda,
                                                             self.dphi)
        return(s)

class GeoGrid3D(object):
    def __init__(self, lat0, lon0, depth0, nlat, nlon, ndepth, dlat, dlon, ddepth):
# NOTE: Origin of spherical coordinate system and geographic coordinate
# system is not the same!
# Geographic coordinate system
        self.lat0, self.lon0, self.depth0 =\
                seispy.coords.as_geographic([lat0, lon0, depth0])
        self.nlat, self.nlon, self.ndepth = nlat, nlon, ndepth
        self.dlat, self.dlon, self.ddepth = dlat, dlon, ddepth
# Spherical/Pseudospherical coordinate systems
        self.nrho = self.ndepth
        self.ntheta = self.nlambda = self.nlat
        self.nphi = self.nlon
        self.drho = self.ddepth
        self.dtheta = self.dlambda = np.radians(self.dlat)
        self.dphi = np.radians(self.dlon)
        self.rho0 = seispy.constants.EARTH_RADIUS\
                - (self.depth0 + (self.ndepth - 1) * self.ddepth)
        self.lambda0 = np.radians(self.lat0)
        self.theta0 = np.pi/2 - (self.lambda0 + (self.nlambda - 1) * self.dlambda)
        self.phi0 = np.radians(self.lon0)

    def __str__(self):
        s = "lat0, lon0, depth0: {:.15g}, {:.15g}, {:.15g}\n".format(self.lat0,
                                                                     self.lon0,
                                                                     self.depth0)
        s += "nlat, nlon, ndepth: {:8d}, {:8d}, {:8d}\n".format(self.nlat,
                                                                self.nlon,
                                                                self.ndepth)
        s += "dlat, dlon, ddepth: {:.15g}, {:.15g}, {:.15g}\n".format(self.dlat,
                                                                      self.dlon,
                                                                      self.ddepth)
        s += "rho0, theta0, lambda0, phi0: {:.15g}, {:.15g}, {:.15g}, {:.15g}\n".format(self.rho0,
                                                                           self.theta0,
                                                                           self.lambda0,
                                                                           self.phi0)
        s += "nrho, ntheta, nlambda, nphi: {:8d} {:8d}, {:8d}, {:8d}\n".format(self.nrho,
                                                                  self.ntheta,
                                                                  self.nlambda,
                                                                  self.nphi)
        s += "drho, dtheta, dlambda, dphi: {:.15g}, {:.15g}, {:.15g}, {:.15g}".format(self.drho,
                                                                         self.dtheta,
                                                                         self.dlambda,
                                                                         self.dphi)
        return(s)

    def fit_subgrid(self,
                    nrho=None,
                    nlat=None,
                    nlon=None):
        nrho = self.nrho if nrho is None else nrho
        nlat = self.ntheta if nlat is None else nlat
        nlon = self.nphi if nlon is None else nlon

        rho0 = self.rho0 + self.drho * 1.01
        rhomax = self.rho0 + (self.nrho - 2.01) * self.drho
        drho = (rhomax - rho0) / (nrho - 1)

        lat0 = self.lat0 + 1.01 * self.dlat
        latmax = self.lat0 + (self.nlat - 2.01) * self.dlat
        dlat = (latmax - lat0) / (nlat - 1)

        lon0 = self.lon0 + self.dlon * 1.01
        lonmax = self.lon0 + (self.nlon - 2.01) * self.dlon
        dlon = (lonmax - lon0) / (nlon - 1)

        return(GeoGrid3D(lat0, lon0, seispy.constants.EARTH_RADIUS - rhomax,
                         nlat, nlon, nrho, dlat, dlon, drho))

def test():
    print(GeoGrid(33.0, -118.0, 6375.0, 25, 25, 25, 0.1, 0.1, 1.0))

if __name__ == "__main__":
    test()
