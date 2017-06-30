import numpy as np
import seispy

class Topography(object):
    """
    A queryable container class to interpolate topographic data on a
    regular grid.
    """
    def __init__(self, infile):
        infile = open(infile)
        R, T, P = [], [], []
        for line in infile:
            lon, lat, elev = [float(v) for v in line.split()]
            r, theta, phi = seispy.geometry.geo2sph(lat, lon, -elev / 1000.)
            R += [r]
            T += [theta]
            P += [phi]
        self.theta = np.array(sorted(list(set(T))))
        self.ntheta = len(self.theta)
        self.theta0 = self.theta[0]
        self.dtheta = (self.theta[-1] - self.theta0) / self.ntheta
        self.phi = np.array(sorted(list(set(P))))
        self.nphi = len(self.phi)
        self.phi0 = self.phi[0]
        self.dphi = (self.phi[-1] - self.phi0) / self.nphi
        self.radius = np.empty(shape=(len(set(T)), len(set(P))))
        for i in range(len(R)):
            itheta = np.where(self.theta == T[i])
            iphi = np.where(self.phi == P[i])
            self.radius[itheta, iphi] = R[i]

    def __call__(self, theta, phi):
        itheta0 = np.argmin(np.absolute(self.theta - theta))
        iphi0 = np.argmin(np.absolute(self.phi - phi))
        dtheta, dphi = itheta % 1, iphi % 1
        itheta1 = min(itheta0 + 1, self.ntheta - 1)
        iphi1 = min(iphi0 + 1, self.nphi - 1)
        T00 = self.radius[itheta0, iphi0]
        T01 = self.radius[itheta0, iphi1]
        T10 = self.radius[itheta1, iphi0]
        T11 = self.radius[itheta1, iphi1]
        T0 = T00 + (T10 - T00) * dtheta
        T1 = T01 + (T11 - T01) * dtheta
        return(T0 + (T1 - T0) * dphi)

if __name__ == "__main__":
    print("WARNING:: topography.py not an executable script")
