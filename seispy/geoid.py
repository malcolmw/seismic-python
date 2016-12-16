import seispy as sp
from math import pi,\
                 radians
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator

class Geoid(object):
    def __init__(self,
                 infile="/home/shake/malcolcw/data/mapping/ANZA/anza.xyz"):
        """
        This container class provides query functionality for surface
        elevation data.
        """
        infile = open(infile)
        R, T, P = [], [], []
        for line in infile:
            lon, lat, elev = [float(v) for v in line.split()]
            r, theta, phi = sp.geometry.geo2sph(lat, lon % 360., -elev / 1000.)
            R += [r]
            T += [theta]
            P += [phi]
        self.theta = np.asarray(sorted(list(set(T))))
        self.ntheta = len(self.theta)
        self.theta0 = min(self.theta)
        self.dtheta = (max(self.theta) - self.theta0) / self.ntheta
        self.phi = np.asarray(sorted(list(set(P))))
        self.nphi = len(self.phi)
        self.phi0 = min(self.phi)
        self.dphi = (max(self.phi) - self.phi0) / self.nphi
        self.radius = np.empty(shape=(len(set(T)), len(set(P))))
        for i in range(len(R)):
            itheta = np.where(self.theta == T[i])
            iphi = np.where(self.phi == P[i])
            self.radius[itheta, iphi] = R[i]
            
    def __call__(self, theta, phi):
        itheta0 = np.argmin(np.absolute(self.theta - theta))
        iphi0 = np.argmin(np.absolute(self.phi - phi))
        deltheta, delphi = itheta0 % 1., iphi0 % 1.
        itheta1 = min(itheta0 + 1, self.ntheta - 1)
        iphi1 = min(iphi0 + 1, self.nphi - 1)
        T00 = self.radius[itheta0, iphi0]
        T01 = self.radius[itheta0, iphi1]
        T10 = self.radius[itheta1, iphi0]
        T11 = self.radius[itheta1, iphi1]
        T0 = T00 + (T10 - T00) * deltheta
        T1 = T01 + (T11 - T01) * deltheta
        return T0 + (T1 - T0) * delphi

    def plot(self):
        f = 4
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        r = np.empty(shape=(self.ntheta * f, self.nphi * f))
        i = 0
        for theta in np.linspace(self.theta0, self.theta0 + (self.ntheta - 1) * self.dtheta, self.ntheta * f):
            j = 0
            for phi in np.linspace(self.phi0, self.phi0 + (self.nphi - 1) * self.dphi, self.nphi * f):
                r[i, j] = self(theta, phi)
                j += 1
            i += 1
        ax.pcolormesh(r[-1:0:-1])
        plt.show()

def test():
    geoid = Geoid()
    geoid.plot()

if __name__ == "__main__":
    test()
