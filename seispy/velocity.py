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
            #self.topo = lambda lat, lon: topo(lat, lon)
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
        self.nodes["ntheta"] = T.shape[1]
        self.nodes["theta_min"] = min(theta_nodes)
        self.nodes["theta_max"] = max(theta_nodes)
        self.nodes["nphi"] = P.shape[2]
        self.nodes["phi_min"] = min(phi_nodes)
        self.nodes["phi_max"] = max(phi_nodes)
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
        # Get indices of closest node to 'below' the point
        cond = lambda v, bounds: bounds[0] < v < bounds[1]
        r_nodes = self.nodes["r"][:,0,0]
        if r <= r_nodes[0]:
            ir0 = 0
            dr = 0
        elif r >= r_nodes[-1]:
            ir0 = len(r_nodes) - 1
            dr = 0
        elif r in r_nodes:
            ir0 = list(r_nodes).index(r)
            dr = 0
        else:
            ir0 = [True if cond(r, b) else False for b in
                    zip(r_nodes[:-1], r_nodes[1:])].index(True)
            dr = r - r_nodes[ir0]

        theta_nodes = self.nodes["theta"][0,:,0]
        if theta <= theta_nodes[0]:
            itheta0 = 0
            dtheta = 0
        elif theta >= theta_nodes[-1]:
            itheta0 = len(theta_nodes) - 1
            dtheta = 0
        elif theta in theta_nodes:
            itheta0 = list(theta_nodes).index(theta)
            dtheta = 0
        else:
            itheta0 = [True if cond(theta, b) else False for b in
                        zip(theta_nodes[:-1], theta_nodes[1:])].index(True)
            dtheta = theta - theta_nodes[itheta0]

        phi_nodes = self.nodes["phi"][0,0,:]
        if phi <= phi_nodes[0]:
            iphi0 = 0
            dphi = 0
        elif phi >= phi_nodes[-1]:
            iphi0 = len(phi_nodes) - 1
            dphi = 0
        elif phi in phi_nodes:
            iphi0 = list(phi_nodes).index(phi)
            dphi = 0
        else:
            iphi0 = [True if cond(phi, b) else False for b in
                    zip(phi_nodes[:-1], phi_nodes[1:])].index(True)
            dphi = phi - phi_nodes[iphi0]
        ir1 = ir0 if ir0 == self.nodes["nr"] - 1 else ir0 + 1
        itheta1 = itheta0 if itheta0 == self.nodes["ntheta"] - 1 else itheta0 + 1
        iphi1 = iphi0 if iphi0 == self.nodes["nphi"] - 1 else iphi0 + 1
        values = self.values[phase]
        V000, V100 = values[ir0, itheta0, iphi0], values[ir1, itheta0, iphi0]
        V010, V110 = values[ir0, itheta1, iphi0], values[ir1, itheta1, iphi0]
        V001, V101 = values[ir0, itheta0, iphi1], values[ir1, itheta0, iphi1]
        V011, V111 = values[ir0, itheta1, iphi1], values[ir1, itheta1, iphi1]
        V100 = V000 if V100 == -1 else V100
        V110 = V010 if V110 == -1 else V110
        V101 = V001 if V101 == -1 else V101
        V111 = V011 if V111 == -1 else V111
        if dr == 0:
            V00, V10, V01, V11 = V000, V010, V001, V011
        else:
            dVdr = (V100 - V000) / (r_nodes[ir1] - r_nodes[ir0])
            V00 = V000 + dVdr * dr
            dVdr = (V110 - V010) / (r_nodes[ir1] - r_nodes[ir0])
            V10 = V010 + dVdr * dr
            dVdr = (V101 - V001) / (r_nodes[ir1] - r_nodes[ir0])
            V01 = V001 + dVdr * dr
            dVdr = (V111 - V011) / (r_nodes[ir1] - r_nodes[ir0])
            V11 = V011 + dVdr * dr
        if dtheta == 0:
            V0, V1 = V00, V01
        else:
            V10 = V00 if V10 == -1 else V10
            V11 = V01 if V11 == -1 else V11
            dVdt = (V10 - V00) / (theta_nodes[itheta1] - theta_nodes[itheta0])
            V0 = V00 + dVdt * dtheta
            dVdt = (V11 - V01) / (theta_nodes[itheta1] - theta_nodes[itheta0])
            V1 = V01 + dVdt * dtheta
        if dphi == 0:
            V = V0
        else:
            V1 = V0 if V1 == -1 else V1
            dVdp = (V1 - V0) / (phi_nodes[iphi1] - phi_nodes[iphi0])
            V = V0 + dVdp * dphi
        return(V)

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

    def regrid(self, R, T, P):
        Vp = np.empty(shape=R.shape)
        Vs = np.empty(shape=R.shape)
        for store, phase, index in ((Vp, "Vp", 0), (Vs, "Vs", 1)):
            for (ir, it, ip) in [(ir, it, ip) for ir in range(R.shape[0])
                                              for it in range(T.shape[1])
                                              for ip in range(P.shape[2])]:
                r, theta, phi = R[ir, it, ip], T[ir, it, ip], P[ir, it, ip]
                store[ir, it, ip] = self._get_V(r, theta, phi, phase)
        self.values["Vp"] = Vp
        self.values["Vs"] = Vs
        self.nodes["r"], self.nodes["theta"], self.nodes["phi"] = R, T, P
        self.nodes["nr"] = R.shape[0]
        self.nodes["ntheta"] = T.shape[1]
        self.nodes["nphi"] = P.shape[2]
        self.nodes["dr"] = (R[:,0,0][-1] - R[:,0,0][0]) / (R.shape[0] - 1)
        self.nodes["dtheta"] = (T[0,:,0][-1] - T[0,:,0][0]) / (T.shape[1] - 1)
        self.nodes["dphi"] = (P[0,0,:][-1] - P[0,0,:][0]) / (P.shape[2] - 1)
        self.nodes["r_min"], self.nodes["r_max"] = np.min(R), np.max(R)
        self.nodes["theta_min"], self.nodes["theta_max"] = np.min(T), np.max(T)
        self.nodes["phi_min"], self.nodes["phi_max"] = np.min(P), np.max(P)

    def regularize(self, nr, ntheta, nphi):
        R, T, P = np.meshgrid(np.linspace(self.nodes["r_min"],
                                          self.nodes["r_max"],
                                          nr),
                              np.linspace(self.nodes["theta_min"],
                                          self.nodes["theta_max"],
                                          ntheta),
                              np.linspace(self.nodes["phi_min"],
                                          self.nodes["phi_max"],
                                          nphi),
                              indexing="ij")
        self.regrid(R, T, P)

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
