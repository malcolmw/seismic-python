from math import degrees,\
                 pi,\
                 radians
import numpy as np
import seispy

class VelocityModel(object):
    def __init__(self, infile, fmt, topo=None):
        if fmt.upper() == "FANG":
            self._read_fang(infile, topo)

    def __call__(self, phase, lat, lon, depth):
        r, theta, phi = seispy.geometry.geo2sph(lat, lon, depth)
        return(self._get_V(r, theta, phi, phase))

    def _read_fang(self, infile, topo):
        if topo is None:
            self.topo = lambda _, __: seispy.constants.EARTH_RADIUS
        else:
            self.topo = topo
        inf = open(infile)
        phi_nodes = [radians(float(lon)) % 360.\
                for lon in inf.readline().split()]
        theta_nodes = [radians(90 - float(lat))\
                for lat in inf.readline().split()]
        r_nodes = [seispy.constants.EARTH_RADIUS - float(z)\
                for z in inf.readline().split()]
        R, T, P = np.meshgrid(r_nodes, theta_nodes, phi_nodes, indexing="ij")
        self.nodes = {"r": R, "theta": T, "phi": P}
        self.nodes["nr"] = R.shape[0]
        self.nodes["r_min"] = min(r_nodes)
        self.nodes["r_max"] = max(r_nodes)
        self.nodes["dr"] = (self.nodes["r_max"] - self.nodes["r_min"]) /\
                (self.nodes["nr"] - 1)
        self.nodes["ntheta"] = T.shape[1]
        self.nodes["theta_min"] = min(theta_nodes)
        self.nodes["theta_max"] = max(theta_nodes)
        self.nodes["dtheta"] = (self.nodes["theta_max"] -\
                self.nodes["theta_min"]) / (self.nodes["ntheta"] - 1)
        self.nodes["nphi"] = P.shape[2]
        self.nodes["phi_min"] = min(phi_nodes)
        self.nodes["phi_max"] = max(phi_nodes)
        self.nodes["dphi"] = (self.nodes["phi_max"] - self.nodes["phi_min"])/\
                (self.nodes["nphi"] - 1)
        self.values = {"Vp": np.empty(shape=(len(r_nodes),
                                             len(theta_nodes),
                                             len(phi_nodes))),
                       "Vs": np.empty(shape=(len(r_nodes),
                                             len(theta_nodes),
                                             len(phi_nodes)))}
        for phase in "Vp", "Vs":
            for (ir, itheta) in [(ir, itheta) for ir in range(self.nodes["nr"])\
                    for itheta in range(self.nodes["ntheta"])]:
                line = inf.readline().split()
                for iphi in range(len(line)):
                    self.values[phase][ir, itheta, iphi] = float(line[iphi])
        # Flip r and theta axis so they increase with increasing index.
        self.nodes["r"] = self.nodes["r"][::-1]
        self.nodes["theta"] = self.nodes["theta"][:,::-1]
        for phase in "Vp", "Vs":
            self.values[phase] = self.values[phase][::-1]
            self.values[phase] = self.values[phase][:,::-1]

    def _get_V(self, r, theta, phi, phase):
        phase = _verify_phase(phase)
        # Make sure 0 <= phi < 2*pi
        phi %= 2 * pi
        if r > self.topo(theta, phi):
            # Return P-wave velocity in air if requested point is above
            # surface.
            return(0.323)
        r = max(r, self.nodes["r_min"])
        theta = min(max(theta, self.nodes["theta_min"]),
                    self.nodes["theta_max"])
        phi = min(max(phi, self.nodes["phi_min"]),
                  self.nodes["phi_max"])
        ir0 = (r - self.nodes["r_min"]) / self.nodes["dr"]
        dr = ir0 % 1.
        ir0 = int(ir0)
        itheta0 = (theta - self.nodes["theta_min"]) / self.nodes["dtheta"]
        dtheta = itheta0 % 1.
        itheta0 = int(itheta0)
        iphi0 = (phi - self.nodes["phi_min"]) / self.nodes["dphi"]
        dphi = iphi0 % 1.
        iphi0 = int(iphi0)
        ir1 = ir0 if ir0 == self.nodes["nr"] - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == self.nodes["ntheta"] - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == self.nodes["nphi"] - 1 else iphi0 + 1
        values = self.values[phase]
        V000, V100 = values[ir0, itheta0, iphi0], values[ir1, itheta0, iphi0]
        V010, V110 = values[ir0, itheta1, iphi0], values[ir1, itheta1, iphi0]
        V001, V101 = values[ir0, itheta0, iphi1], values[ir1, itheta0, iphi1]
        V011, V111 = values[ir0, itheta1, iphi1], values[ir1, itheta1, iphi1]
        V00 = V000 + (V100 - V000) * dr
        V10 = V010 + (V110 - V010) * dr
        V01 = V001 + (V101 - V001) * dr
        V11 = V011 + (V111 - V011) * dr
        V0 = V00 + (V10 - V00) * dtheta
        V1 = V01 + (V11 - V01) * dtheta
        return(V0 + (V1 - V0) * dphi)

    def get_grid_center(self):
        return ((self.nodes["r_max"] + self.nodes["r_min"]) / 2,
                (self.nodes["theta_max"] + self.nodes["theta_min"]) / 2,
                (self.nodes["phi_max"] + self.nodes["phi_min"]) / 2)

    def slice(self, phase, lat0, lon0, azimuth, length, dmin, dmax, nx, nd):
        (lon1, lat1), (lon2, lat2) = seispy.geometry.get_line_endpoints(lat0,
                                                                        lon0,
                                                                        azimuth,
                                                                        length)
        DEPTH = np.linspace(dmin, dmax, nd)
        LAT = np.linspace(lat1, lat2, nx)
        LON = np.linspace(lon1, lon2, nx)
        V = np.empty(shape=(len(DEPTH), len(LAT)))
        X = np.empty(shape=V.shape)
        Y = np.empty(shape=V.shape)
        for i in range(nx):
            for j in range(nd):
                lat, lon, depth = LAT[i], LON[i], DEPTH[j]
                V[i, j] = self(phase, lat, lon, depth)
                X[i, j] = seispy.geometry.distance((lat1, lon1), (lat, lon))
                Y[i, j] = depth
        return(X, Y, V)

def _verify_phase(phase):
    if phase.upper() == "P" or  phase.upper() == "VP":
        phase = "Vp"
    elif phase.upper() == "S" or phase.upper() == "VS":
        phase = "Vs"
    else:
        raise(ValueError("invalid phase type - {}".format(phase)))
    return(phase)
