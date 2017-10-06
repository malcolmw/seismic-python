from math import degrees,\
                 pi,\
                 radians
import numpy as np
import scipy.interpolate
import seispy

π = np.pi

class VelocityModel(object):
    def __init__(self, inf, fmt, topo=None):
        """
        A callable class providing a queryable container for seismic
        velocities in a 3D volume.

        :param str inf: path to input file containing phase velocity
                           data
        :param str fmt: format of input file
        """
        if topo is None:
            self.topo = lambda _, __: seispy.constants.EARTH_RADIUS
        else:
            self.topo = topo

        if fmt.upper() == "FANG":
            self._read_fang(inf)
        elif fmt.upper() == "FM3D" or fmt.upper() == "FMM3D":
            self._read_fmm3d(inf)

    def __call__(self, typeID, gridID, lat, lon, depth):
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

        rho, theta, phi = seispy.coords.as_geographic([lat, lon, depth]).to_spherical()
        return(self._get_V(rho, theta, phi, typeID, gridID))

    def __str__(self):
        s = "{} {}\n".format(self.nvgrids, self.nvtypes)
        for gridID in range(1, self.nvgrids + 1):
            for typeID in range(1, self.nvtypes + 1):
                model = self.v_type_grids[typeID][gridID]
                grid = model["grid"]
                data = model["data"]
                s += "{} {} {}\n".format(grid.nrho, grid.nlambda, grid.nphi)
                s += "{:g} {:g} {:g}\n".format(grid.drho, grid.dlambda, grid.dphi)
                s += "{:g} {:g} {:g}\n".format(grid.rho0, grid.lambda0, grid.phi0)
                for (irho, ilambda, iphi) in [(irho, ilambda, iphi) for irho in range(grid.nrho)
                                                  for ilambda in range(grid.nlambda)
                                                  for iphi in range(grid.nphi)]:
                    s += "{:g}\n".format(data[irho, ilambda, iphi])
        return(s)

    def _read_fmm3d(self, inf):
        inf = open(inf, "r")
        self.nvgrids, self.nvtypes = [int(v) for v in inf.readline().split()[:2]]
        self.v_type_grids = {}
        for (typeID, gridID) in [(ivt, ivg) for ivt in range(1, self.nvtypes+1)
                                            for ivg in range(1, self.nvgrids+1)]:
            if typeID not in self.v_type_grids:
                self.v_type_grids[typeID] = {}
            model = {"typeID": typeID, "gridID": gridID}
            nrho, nlambda, nphi = [int(v) for v in inf.readline().split()[:3]]
            drho, dlambda, dphi = [float(v) for v in inf.readline().split()[:3]]
            rho0, lambda0, phi0 = [float(v) for v in inf.readline().split()[:3]]
            model["grid"] = seispy.geogrid.GeoGrid3D(np.degrees(lambda0),
                                              np.degrees(phi0),
                                              seispy.constants.EARTH_RADIUS - (rho0 + (nrho-1)*drho),
                                              nlambda, nphi, nrho,
                                              np.degrees(dlambda),
                                              np.degrees(dphi),
                                              drho)
            #model["coords"] = coords.SphericalCoordinates((nrho, nlambda, nphi))
            #model["coords"][...] = [[[[rho0 + irho * drho, π/2 - (lambda0 + ilambda * dlambda), phi0 + iphi * dphi]
            #                           for iphi in range(nphi)]
            #                           for ilambda in range(nlambda)]
            #                           for irho in range(nrho)]
            #model["coords"] = np.flip(model["coords"], axis=1)
            model["data"] = np.empty((nrho, nlambda, nphi))
            model["data"][...] = [[[float(inf.readline().split()[0])
                                    for iphi in range(nphi)]
                                    for ilambda in range(nlambda)]
                                    for irho in range(nrho)]
            model["data"] = np.flip(model["data"], axis=1)
            self.v_type_grids[typeID][gridID] = model

    def _read_fang(self, inf):
        inf = open(inf)
        self.nvgrids, self.nvtypes = 1, 2
        self.v_type_grids = {1: {}, 2: {}}
        phi_nodes = [radians(float(lon))\
                for lon in inf.readline().split()]
        theta_nodes = [radians(90 - float(lat))\
                for lat in inf.readline().split()]
        r_nodes = [seispy.constants.EARTH_RADIUS - float(z)\
                for z in inf.readline().split()]
        phi_nodes = [phi - 2*π if phi > π else phi for phi in phi_nodes]
        R, T, P = np.meshgrid(r_nodes, theta_nodes, phi_nodes, indexing="ij")
        nodes = {"r": R, "theta": T, "phi": P}
        values = {1: np.empty(shape=(len(r_nodes),
                                     len(theta_nodes),
                                     len(phi_nodes))),
                  2: np.empty(shape=(len(r_nodes),
                                     len(theta_nodes),
                                     len(phi_nodes)))}
        for vtype in (1, 2):
            for (ir, itheta) in [(ir, itheta) for ir in range(len(r_nodes))\
                                      for itheta in range(len(theta_nodes))]:
                line = inf.readline().split()
                for iphi in range(len(line)):
                    values[vtype][ir, itheta, iphi] = float(line[iphi])
        # Flip r and theta axis so they increase with increasing index.
        nodes["r"] = nodes["r"][::-1]
        nodes["theta"] = nodes["theta"][:,::-1]
        for vtype in (1, 2):
            values[vtype] = values[vtype][::-1]
            values[vtype] = values[vtype][:,::-1]
        nrho, nlambda, nphi = len(r_nodes), len(theta_nodes), len(phi_nodes)
        drho = (max(r_nodes) - min(r_nodes)) / (nrho - 1)
        dlambda = (max(theta_nodes) - min(theta_nodes)) / (nlambda - 1)
        dphi = (max(phi_nodes) - min(phi_nodes)) / (nphi - 1)
        rho0 = seispy.constants.EARTH_RADIUS - max(r_nodes)
        lambda0 = π/2 - max(theta_nodes)
        phi0 = min(phi_nodes)
        for vtype in (1, 2):
            model = {"typeID": vtype, "gridID": 1}
            model["grid"] = seispy.geogrid.GeoGrid3D(np.degrees(lambda0),
                                                     np.degrees(phi0),
                                                     rho0,
                                                     nlambda, nphi, nrho,
                                                     np.degrees(dlambda),
                                                     np.degrees(dphi),
                                                     drho)
            grid = model["grid"]
            model["data"] = np.empty((nrho, nlambda, nphi))
            for (irho, ilambda, iphi) in [(irho, ilambda, iphi)\
                                    for irho in range(nrho)\
                                    for ilambda in range(nlambda)\
                                    for iphi in range(nphi)]:
                r = grid.rho0 + irho * grid.drho
                theta = π/2 - (grid.lambda0 + ilambda * grid.dlambda)
                phi = grid.phi0 + iphi * grid.dphi

                if r < min(r_nodes):
                    ir0 = 0
                else:
                    ir0 = [i for i in range(len(r_nodes))
                             if nodes["r"][i, 0, 0] <= r][-1]
                if r > max(r_nodes):
                    ir1 = len(r_nodes) - 1
                else:
                    ir1 = [i for i in range(len(r_nodes))
                             if nodes["r"][i, 0, 0] >= r][0]
                δr = r - nodes["r"][ir0, 0, 0]
                Δr = nodes["r"][ir1, 0, 0] - nodes["r"][ir0, 0, 0]

                if theta < min(theta_nodes):
                    itheta0 = 0
                else:
                    itheta0 = [i for i in range(len(theta_nodes))
                             if nodes["theta"][0, i, 0] <= theta][-1]
                if theta > max(theta_nodes):
                    itheta1 = len(theta_nodes) - 1
                else:
                    itheta1 = [i for i in range(len(theta_nodes))
                             if nodes["theta"][0, i, 0] >= theta][0]
                δtheta = theta - nodes["theta"][0, itheta0, 0]
                Δtheta = nodes["theta"][0, itheta1, 0] - nodes["theta"][0, itheta0, 0]

                if phi < min(phi_nodes):
                    iphi0 = 0
                else:
                    iphi0 = [i for i in range(len(phi_nodes))
                             if nodes["phi"][0, 0, i] <= phi][-1]
                if phi > max(phi_nodes):
                    iphi1 = len(phi_nodes) - 1
                else:
                    iphi1 = [i for i in range(len(phi_nodes))
                             if nodes["phi"][0, 0, i] >= phi][0]
                δphi = phi - nodes["phi"][0, 0, iphi0]
                Δphi = nodes["phi"][0, 0, iphi1] - nodes["phi"][0, 0, iphi0]

                V000 = values[vtype][ir0, itheta0, iphi0]
                V001 = values[vtype][ir0, itheta0, iphi1]
                V010 = values[vtype][ir0, itheta1, iphi0]
                V011 = values[vtype][ir0, itheta1, iphi1]
                V100 = values[vtype][ir1, itheta0, iphi0]
                V101 = values[vtype][ir1, itheta0, iphi1]
                V110 = values[vtype][ir1, itheta1, iphi0]
                V111 = values[vtype][ir1, itheta1, iphi1]

                if Δr == 0:
                    V00 = V000
                    V01 = V001
                    V10 = V010
                    V11 = V011
                else:
                    V00 = V000 + (V100 - V000) * δr / Δr
                    V01 = V001 + (V101 - V001) * δr / Δr
                    V10 = V010 + (V110 - V010) * δr / Δr
                    V11 = V011 + (V111 - V011) * δr / Δr

                if Δtheta == 0:
                    V0 = V00
                    V1 = V01
                else:
                    V0 = V00 + (V10 - V00) * δtheta / Δtheta
                    V1 = V01 + (V11 - V01) * δtheta / Δtheta

                if Δphi == 0:
                    V = V0
                else:
                    V = V0 + (V1 - V0)*dphi

                model["data"][irho, ilambda, iphi] = V
            model["data"] = np.flip(model["data"], axis=1)
            self.v_type_grids[vtype][1] = model

    def _read_fang_dep(self, inf, topo):
        """
        Initialize velocity model from data in Fang et al. (2016)
        format file.

        :param str inf: path to input file containing phase velocity
                           data
        :param `seispy.topography.Topography` topo: surface elevation
                                                    data
        """
        inf = open(inf)
        phi_nodes = [radians(float(lon))\
                for lon in inf.readline().split()]
        theta_nodes = [radians(90 - float(lat))\
                for lat in inf.readline().split()]
        r_nodes = [seispy.constants.EARTH_RADIUS - float(z)\
                for z in inf.readline().split()]
        phi_nodes = [phi - 2*π if phi > π else phi for phi in phi_nodes]
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

    def _get_V(self, rho, theta, phi, typeID, gridID):
        if isinstance(typeID, str):
            if typeID.upper() in ("P", "VP"):
                typeID = 1
            elif typeID.upper() in ("S", "VS"):
                typeID = 2
        model = self.v_type_grids[typeID][gridID]["data"]
        grid = self.v_type_grids[typeID][gridID]["grid"]

        irho = (rho - grid.rho0)/grid.drho
        irho0 = min(max(int(np.floor(irho)), 0), grid.nrho - 1)
        irho1 = max(min(int(np.ceil(irho)), grid.nrho - 1), 0)
        drho = irho - irho0

        itheta = (theta - grid.theta0)/grid.dtheta
        itheta0 = min(max(int(np.floor(itheta)), 0), grid.ntheta - 1)
        itheta1 = max(min(int(np.ceil(itheta)), grid.ntheta - 1), 0)
        dtheta = itheta - itheta0
        #print(theta, itheta, itheta0, itheta1, grid.ntheta)

        iphi = (phi - grid.phi0)/grid.dphi
        iphi0 = min(max(int(np.floor(iphi)), 0), grid.nphi - 1)
        iphi1 = max(min(int(np.ceil(iphi)), grid.nphi - 1), 0)
        dphi = iphi - iphi0

        V000 = model[irho0,itheta0,iphi0]
        V001 = model[irho0,itheta0,iphi1]
        V010 = model[irho0,itheta1,iphi0]
        V011 = model[irho0,itheta1,iphi1]
        V100 = model[irho1,itheta0,iphi0]
        V101 = model[irho1,itheta0,iphi1]
        V110 = model[irho1,itheta1,iphi0]
        V111 = model[irho1,itheta1,iphi1]

        V00 = V000 + (V100 - V000)*drho
        V01 = V001 + (V101 - V001)*drho
        V10 = V010 + (V110 - V010)*drho
        V11 = V011 + (V111 - V011)*drho

        V0 = V00 + (V10 - V00)*dtheta
        V1 = V01 + (V11 - V01)*dtheta

        V = V0 + (V1 - V0)*dphi

        return(V)

    def _get_V_dep(self, r, theta, phi, phase):
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
        phi -= 2 * pi
        if r > self.topo(*seispy.coords.as_spherical([r, theta, phi]).to_geographic()[:2]):
            # Return a null value if requested point is above surface.
            #return(-1)
            return(1)
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
            V0 = V00 + dVdt * dtheta / r
            dVdt = (V11 - V01) / (theta_nodes[itheta1] - theta_nodes[itheta0])
            V1 = V01 + dVdt * dtheta / r
        if dphi == 0:
            V = V0
        else:
            V1 = V0 if V1 == -1 else V1
            dVdp = (V1 - V0) / (phi_nodes[iphi1] - phi_nodes[iphi0])
            V = V0 + dVdp * dphi / (r * np.sin(theta))
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
                           180]*\ **}**
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

def test():
    #vm = VelocityModel("/Users/malcolcw/Projects/Wavefront/examples/example2/vgrids.in", "fmm3d")
    #grid = vm.v_type_grids[1][1]["grid"]
    #print(vm(1, 3, 0.5, 0.5, 0))
    #vm.v_type_grids[1][1]
    #print(v("Vp", 33.0, -116.9, 3.0))
    vm = VelocityModel("/Users/malcolcw/Projects/Shared/Velocity/FANG2016/original/VpVs.dat", "fang")
    with open("/Users/malcolcw/Projects/Wavefront/pywrap/example5/vgrids.in", "w") as outf:
        outf.write(str(vm))
if __name__ == "__main__":
    test()
    print("velocity.py is not an executable script.")
    exit()
