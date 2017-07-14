from math import degrees,\
                 pi,\
                 radians
import numpy as np
import seispy

class VelocityModel(object):
    def __init__(self, infile, fmt, topo=None):
        """
        A callable class providing a queryable container for seismic
        velocities in a 3D volume.

        :param str infile: path to input file containing phase velocity
                           data
        :param str fmt: format of input file
        """
        if fmt.upper() == "FANG":
            self._read_fang(infile, topo)

    def __call__(self, phase, lat, lon, depth):
        """
        Return **phase**-velocity at given coordinates. A NULL value
        (-1) is returned for points above the surface.

        :param str phase: phase
        :param float lat: latitude
        :param float lon: longitude
        :param float depth: depth
        :returns: **phase**-velocity at (**lat**, **lon**, **depth**)
        :rtype: float
        """

        r, theta, phi = seispy.geometry.geo2sph(lat, lon, depth)
        return(self._get_V(r, theta, phi, phase))

    def _read_fang(self, infile, topo):
        """
        Initialize velocity model from data in Fang et al. (2016)
        format file.

        :param str infile: path to input file containing phase velocity
                           data
        :param `seispy.topography.Topography` topo: surface elevation
                                                    data
        """
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
        """
        Return `phase` velocity at spherical coordinates (`r`, `theta`,
        `phi`).  Geographic coordinates can be converted to spherical
        coordinates using `seispy.geometry.geo2sph`.

        :param float r: Radial distance from coordinate system origin.
        :param float theta: Polar angle [0, pi].
        :param float phi: Azimuthal angle [0, 2*pi].
        :param str phase: Seismic phase ["P", "S", "Vp", "Vs"].
        """
        phase = _verify_phase(phase)
        # Make sure 0 <= phi < 2*pi
        phi %= 2 * pi
        if r > self.topo(*seispy.geometry.sph2geo(r, theta, phi)[:2]):
            # Return a null value if requested point is above surface.
            return(-1)
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
        """
        Return the center of the velocity model in spherical
        coordinates (r, theta, phi).

        :returns: coordinates of velocity model center in spherical
                  coordinates
        :rtype: (float, float, float)

        """
        return ((self.nodes["r_max"] + self.nodes["r_min"]) / 2,
                (self.nodes["theta_max"] + self.nodes["theta_min"]) / 2,
                (self.nodes["phi_max"] + self.nodes["phi_min"]) / 2)

    def slice(self, phase, lat0, lon0, azimuth, length, dmin, dmax, nx, nd):
        """
        Return a vertical slice from velocity model with
        section-parallel offset and depth coordinates.

        :param str phase: phase velocity to retrieve
        :param float lat0: latitude of center point of section trace
                           **{Units:** *degrees*, **Range:** *[-90, 90]*\
                           **}**
        :param float lon0: longitude of center point of section trace
                           **{Units:** *degrees*, **Range:** *[-180,
                           360)*\ **}**
        :param float azimuth: azimuth of section trace **{Units:**
                              *degrees*, **Range:** *(-inf, inf)*\ **}**
        :param float length: length of section trace **{Units:**
                             *degrees*\ **}**
        :param float dmin: minimum depth of section **{Units:** *km*\
                           **}**
        :param float dmax: maximum depth of section **{Units:** *km*\
                           **}**
        :param int nx: number of nodes in section-parallel direction
        :param int nd: number of nodes in depth
        :returns: phase velocity values and coordinates of vertical
                  section
        :rtype: (`numpy.ndarray`, `numpy.ndarray`, `numpy.ndarray`)

        .. code-block:: python

            import matplotlib.pyplot as plt
            topo = seispy.topography.Topography("data/anza.xyz")
            vm = seispy.velocity.VelocityModel("data/vmodel.dat",
                                               "FANG",
                                               topo=topo)
            X, Y, V = vm.slice("P", 33.5, -116.0, 302, 150/111, -5, 25, 100, 100)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            im = ax.pcolormesh(X, Y, V, cmap=plt.get_cmap("hsv"))
            ax.set_xlabel("Section-parallel offset [degrees]")
            ax.set_ylabel("Depth [km]")
            ax.invert_yaxis()
            cbar = ax.get_figure().colorbar(im, ax=ax)
            cbar.set_label("Vp [km/s]")
            plt.show()

        .. image:: VelocityModel.png
        """

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
        V = np.ma.masked_equal(V, -1)
        return(X, Y, V)

def _verify_phase(phase):
    if phase.upper() == "P" or  phase.upper() == "VP":
        phase = "Vp"
    elif phase.upper() == "S" or phase.upper() == "VS":
        phase = "Vs"
    else:
        raise(ValueError("invalid phase type - {}".format(phase)))
    return(phase)
