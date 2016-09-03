#from seispy.geometry import deg2rad,\
from geometry import deg2rad,\
                            EARTH_RADIUS,\
                            geo2sph
from numpy import zeros

class VelocityModel(object):
    """
    This class is intended to facilitate querying and plotting of velocity models.

    For now, assume a model defined on a regular grid in spherical coordinates.

    .. todo::
       document this class.
    """
    def __init__(self, infile, fmt='fang'):
        if fmt.upper() == 'FANG':
            self._read_fang(infile)

    def _read_fang(self, infile):
        infile = open(infile)
        lon_nodes = [float(lon) for lon in infile.readline().split()]
        for i in range(len(lon_nodes)):
            if lon_nodes[i] < -180.:
                lon_nodes[i] += 360.
            elif lon_nodes[i] > 360.:
                lon_nodes[i] -= 360.
        lat_nodes = [float(lat) for lat in infile.readline().split()]
        z_nodes = [float(z) for z in infile.readline().split()]
        r_nodes = [EARTH_RADIUS - z for z in z_nodes]
        theta_nodes = [deg2rad(90. - lat) for lat in lat_nodes]
        phi_nodes = [deg2rad(lon) for lon in lon_nodes]
        self.model = {
            'Vp': zeros((len(r_nodes), len(theta_nodes), len(phi_nodes))),
            'Vs': zeros((len(r_nodes), len(theta_nodes), len(phi_nodes)))
            }
        self.nodes = zeros((len(r_nodes), len(theta_nodes), len(phi_nodes)),
                           dtype='float32, float32, float32')
        #initalize the grid of node coordinates
        for ir in range(len(r_nodes)):
            for itheta in range(len(theta_nodes)):
                for iphi in range(len(phi_nodes)):
                    self.nodes[ir, itheta, iphi] = (r_nodes[ir],
                                                    theta_nodes[itheta],
                                                    phi_nodes[iphi])
        #initialize the grids of velocity values
        for phase in ('Vp', 'Vs'):
            for ir in range(len(r_nodes)):
                for itheta in range(len(theta_nodes)):
                    line = infile.readline().split()
                    for iphi in range(len(line)):
                        self.model[phase][ir, itheta, iphi] = float(line[iphi])

    def _get_V(self, r, theta, phi, phase):
        if r > self.nodes[0, 0, 0][0]\
                or r < self.nodes[-1, 0, 0][0]\
                or theta > self.nodes [0, 0, 0][1]\
                or theta < self.nodes[0, -1, 0][1]\
                or phi < self.nodes[0, 0, 0][2]\
                or phi > self.nodes[0, 0, -1][2]:
            raise ValueError("point lies outside velocity model")
        ir0, itheta0, iphi0 = None, None, None
        for ir in range(self.nodes.shape[0] - 1):
            if self.nodes[ir, 0, 0][0] > r > self.nodes[ir + 1, 0, 0][0]:
                ir0 = ir
                break
        for itheta in range(self.nodes.shape[1] - 1):
            if self.nodes[0, itheta, 0][1] > theta > self.nodes[0, itheta + 1, 0][1]:
                itheta0 = itheta
                break
        for iphi in range(self.nodes.shape[2] - 1):
            if self.nodes[0, 0, iphi][2] > phi > self.nodes[0, 0, phi + 1][2]:
                iphi0 = iphi
                break
        if not ir0:
            ir0 = [n[0] for n in self.nodes[:, 0, 0]].index(r)
        if not itheta0:
            itheta0 = [n[1] for n in self.nodes[0, :, 0]].index(theta)
        if not iphi0:
            iphi0 = [n[2] for n in self.nodes[0, 0, :]].index(phi)
        #still need to deal with edges properly
        #do a trilinear interpolation
        model = self.model[phase]
        V000 = model[ir0, itheta0, iphi0]
        V100 = model[ir0 + 1, itheta0, iphi0]
        V010 = model[ir0, itheta0 + 1, iphi0]
        V110 = model[ir0 + 1, itheta0 + 1, iphi0]
        V001 = model[ir0, itheta0, iphi0 + 1]
        V101 = model[ir0 + 1, itheta0, iphi0 + 1]
        V011 = model[ir0, itheta0 + 1, iphi0 + 1]
        V111 = model[ir0 + 1, itheta0 + 1, iphi0 + 1]
        dV00 = V100 - V000
        dV10 = V110 - V010
        dV01 = V101 - V001
        dV11 = V111 - V011
        dr = self.nodes[ir0 + 1, 0, 0][0] - self.nodes[ir0, 0, 0][0]
        delta_r = r - self.nodes[ir0, 0, 0][0]
        V00 = V000 + (dV00 / dr) * delta_r
        V10 = V010 + (dV10 / dr) * delta_r
        V01 = V001 + (dV01 / dr) * delta_r
        V11 = V011 + (dV11 / dr) * delta_r
        dV0 = V10 - V00
        dV1 = V11 - V01
        dtheta = self.nodes[0, itheta + 1, 0][1] - self.nodes[0, itheta, 0][1]
        delta_theta = theta - self.nodes[0, itheta, 0][1]
        V0 = V00 + (dV0 / dtheta) * delta_theta
        V1 = V01 + (dV1 / dtheta) * delta_theta
        dV = V1 - V0
        dphi = self.nodes[0, 0, iphi + 1][2] - self.nodes[0, 0, iphi][2]
        delta_phi = phi - self.nodes[0, 0, phi][2]
        V = V0 + (dV / dphi) * delta_phi
        return V

    def get_Vp(self, lat, lon, depth):
        r, theta, phi = geo2sph(lat, lon, depth)
        return self._get_V(r, theta, phi, 'Vp')

    def get_Vs(self):
        pass

    def _plot(self, lat, lon, depth, phase):
        if lat == -999 and lon == -999:
            #plot depth slice
            pass
        elif lat == -999 and depth == -999:
            #plot longitudinal slice
            pass
        elif lon == -999 and depth == -999:
            #plot latitudinal slice
            pass

    def plot_Vp(self, lat=-999, lon=-999, depth=-999):
        pass

    def plot_Vs(self):
        pass

    def plot_VpVs_ratio(self):
        pass
