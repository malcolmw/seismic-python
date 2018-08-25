# coding=utf-8
import numpy as np
import seispy

class GeoSurface(object):
    """
    A queryable container class to interpolate topographic data on a
    regular grid.
    """
    def __init__(self):
        pass

    def _callable(self, lat, lon):
# HACK
# THIS NEEDS TO BE CLEANED UP
        #lon = lon % 360 - 360
        _, theta, phi = seispy.coords.as_geographic([lat, lon, 0]).to_spherical()
        itheta = (theta - self.grid.theta0) / self.grid.dtheta
        itheta0 = int(min([max([0, np.floor(itheta)]), self.grid.ntheta - 1]))
        itheta1 = int(max([0, min([self.grid.ntheta-1, np.ceil(itheta)])]))
        iphi = (phi - self.grid.phi0) / self.grid.dphi
        iphi0 = int(min([max([0, np.floor(iphi)]), self.grid.nphi - 1]))
        iphi1 = int(max([0, min([self.grid.nphi, np.ceil(iphi)])]))
        R00 = self.coordinates[itheta0, iphi0, 0]
        R01 = self.coordinates[itheta0, iphi1, 0]
        R10 = self.coordinates[itheta1, iphi0, 0]
        R11 = self.coordinates[itheta1, iphi1, 0]
        dtheta = theta - self.coordinates[itheta0, iphi0, 1]
        dphi = phi - self.coordinates[itheta0, iphi0, 2]
        R0 = R00 + (R10 - R00) * dtheta
        R1 = R01 + (R11 - R01) * dtheta
        return(R0 + (R1 - R0) * dphi)

    def read(self, infile):
        infile = open(infile)
        LAT, LON, DEPTH = [], [], []
        COORDINATES = np.empty((0, 3))
        for line in infile:
            COORDINATES = np.append(COORDINATES,
                                    [[float(v) for v in line.split()]],
                                    axis=0)
        COORDINATES[:,2] *= -1/1000
        COORDINATES[:,[0,1]] = COORDINATES[:,[1,0]]
        COORDINATES = seispy.coords.as_geographic(COORDINATES)
        nlat = len(np.unique(COORDINATES[:,0]))
        nlon = len(np.unique(COORDINATES[:,1]))
        minlat = COORDINATES[:,0].min()
        minlon = COORDINATES[:,1].min()
        maxlat = COORDINATES[:,0].max()
        maxlon = COORDINATES[:,1].max()
        dlat = (maxlat - minlat) / (nlat - 1)
        dlon = (maxlon - minlon) / (nlon - 1)
        self.grid = seispy.geogrid.GeoGrid2D(minlat, minlon, nlat, nlon, dlat, dlon)
        COORDINATES = COORDINATES.to_spherical()
        COORDINATES = np.array(sorted(COORDINATES, key=lambda c: (c[1], c[2])))
        COORDINATES = COORDINATES.reshape((nlat, nlon, 3))
        self.coordinates = COORDINATES


    def __call__(self, lat, lon):
        return(self._callable(lat, lon))

def test():
    geosurf = GeoSurface()
    geosurf.read("/Users/malcolcw/Projects/Shared/Topography/anza.xyz")
    print(geosurf(33.0, -116.0))
    print(geosurf.grid.theta0)

if __name__ == "__main__":
    print("WARNING:: topography.py not an executable script")
