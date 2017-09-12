import numpy as np
import seispy

π = np.pi

class GeoGrid2D(object):
    def __init__(self, lat0, lon0, nlat, nlon, dlat, dlon):
# NOTE: Origin of spherical coordinate system and geographic coordinate
# system is not the same!
# Geographic coordinate system
        self.lat0, self.lon0, _ = seispy.coords.as_geographic([lat0, lon0, 0])
        self.nlat, self.nlon = nlat, nlon
        self.dlat, self.dlon = dlat, dlon
# Spherical/Pseudospherical coordinate systems
        self.nθ = self.nλ = self.nlat
        self.nφ = self.nlon

        self.dθ = self.dλ = np.radians(self.dlat)
        self.dφ = np.radians(self.dlon)

        self.λ0 = np.radians(self.lat0)
        self.θ0 = np.pi/2 - (self.λ0 + (self.nλ - 1) * self.dλ)
        self.φ0 = np.radians(self.lon0)

    def __str__(self):
        s = "lat0, lon0: {:.15g}, {:.15g}\n".format(self.lat0,
                                                    self.lon0)
        s += "nlat, nlon: {:8d}, {:8d}\n".format(self.nlat,
                                                 self.nlon)
        s += "dlat, dlon: {:.15g}, {:.15g}\n".format(self.dlat,
                                                     self.dlon)
        s += "θ0, λ0, φ0: {:.15g}, {:.15g}, {:.15g}\n".format(self.θ0,
                                                             self.λ0,
                                                             self.φ0)
        s += "nθ, nλ, nφ : {:8d}, {:8d}\n".format(self.nθ,
                                                  self.nλ,
                                                  self.nφ)
        s += "dθ, dλ, dφ : {:.15g}, {:.15g}, {:.15g}".format(self.dθ,
                                                             self.dλ,
                                                             self.dφ)
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
        self.nρ = self.ndepth
        self.nθ = self.nλ = self.nlat
        self.nφ = self.nlon
        self.dρ = self.ddepth
        self.dθ = self.dλ = np.radians(self.dlat)
        self.dφ = np.radians(self.dlon)
        self.ρ0 = seispy.constants.EARTH_RADIUS\
                - (self.depth0 + (self.ndepth - 1) * self.ddepth)
        self.λ0 = np.radians(self.lat0)
        self.θ0 = π/2 - (self.λ0 + (self.nλ - 1) * self.dλ)
        self.φ0 = np.radians(self.lon0)

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
        s += "ρ0, θ0, λ0, φ0: {:.15g}, {:.15g}, {:.15g}, {:.15g}\n".format(self.ρ0,
                                                                           self.θ0,
                                                                           self.λ0,
                                                                           self.φ0)
        s += "nρ, nθ, nλ, nφ: {:8d} {:8d}, {:8d}, {:8d}\n".format(self.nρ,
                                                                  self.nθ,
                                                                  self.nλ,
                                                                  self.nφ)
        s += "dρ, dθ, dλ, dφ: {:.15g}, {:.15g}, {:.15g}, {:.15g}".format(self.dρ,
                                                                         self.dθ,
                                                                         self.dλ,
                                                                         self.dφ)
        return(s)

    def fit_subgrid(self,
                    nρ=None,
                    nlat=None,
                    nlon=None):
        nρ = self.nρ if nρ is None else nρ
        nlat = self.nθ if nlat is None else nlat
        nlon = self.nφ if nlon is None else nlon

        ρ0 = self.ρ0 + self.dρ * 1.01
        ρmax = self.ρ0 + (self.nρ - 2.01) * self.dρ
        dρ = (ρmax - ρ0) / (nρ - 1)

        lat0 = self.lat0 + 1.01 * self.dlat
        latmax = self.lat0 + (self.nlat - 2.01) * self.dlat
        dlat = (latmax - lat0) / (nlat - 1)

        lon0 = self.lon0 + self.dlon * 1.01
        lonmax = self.lon0 + (self.nlon - 2.01) * self.dlon
        dlon = (lonmax - lon0) / (nlon - 1)

        return(GeoGrid3D(lat0, lon0, seispy.constants.EARTH_RADIUS - ρmax,
                         nlat, nlon, nρ, dlat, dlon, dρ))

def test():
    print(GeoGrid(33.0, -118.0, 6375.0, 25, 25, 25, 0.1, 0.1, 1.0))

if __name__ == "__main__":
    test()
