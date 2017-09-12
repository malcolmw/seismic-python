from math import degrees,\
                 pi,\
                 radians
import numpy as np
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

        r, θ, φ = seispy.coords.as_geographic([lat, lon, depth]).to_spherical()
        return(self._get_V(r, θ, φ, typeID, gridID))

    def _read_fmm3d(self, inf):
        inf = open(inf, "r")
        self.nvgrids, self.nvtypes = [int(v) for v in inf.readline().split()[:2]]
        self.v_type_grids = {}
        for (typeID, gridID) in [(ivt, ivg) for ivt in range(1, self.nvtypes+1)
                                            for ivg in range(1, self.nvgrids+1)]:
            if typeID not in self.v_type_grids:
                self.v_type_grids[typeID] = {}
            model = {"typeID": typeID, "gridID": gridID}
            nρ, nλ, nφ = [int(v) for v in inf.readline().split()[:3]]
            dρ, dλ, dφ = [float(v) for v in inf.readline().split()[:3]]
            ρ0, λ0, φ0 = [float(v) for v in inf.readline().split()[:3]]
            model["grid"] = seispy.geogrid.GeoGrid3D(np.degrees(λ0),
                                              np.degrees(φ0),
                                              seispy.constants.EARTH_RADIUS - (ρ0 + (nρ-1)*dρ),
                                              nλ, nφ, nρ,
                                              np.degrees(dλ),
                                              np.degrees(dφ),
                                              dρ)
            #model["coords"] = coords.SphericalCoordinates((nρ, nλ, nφ))
            #model["coords"][...] = [[[[ρ0 + iρ * dρ, π/2 - (λ0 + iλ * dλ), φ0 + iφ * dφ]
            #                           for iφ in range(nφ)]
            #                           for iλ in range(nλ)]
            #                           for iρ in range(nρ)]
            #model["coords"] = np.flip(model["coords"], axis=1)
            model["data"] = np.empty((nρ, nλ, nφ))
            model["data"][...] = [[[float(inf.readline().split()[0])
                                    for iφ in range(nφ)]
                                    for iλ in range(nλ)]
                                    for iρ in range(nρ)]
            model["data"] = np.flip(model["data"], axis=1)
            self.v_type_grids[typeID][gridID] = model

    def _read_fang(self, inf, topo):
        """
        Initialize velocity model from data in Fang et al. (2016)
        format file.

        :param str inf: path to input file containing phase velocity
                           data
        :param `seispy.topography.Topography` topo: surface elevation
                                                    data
        """
        inf = open(inf)
        φ_nodes = [radians(float(lon))\
                for lon in inf.readline().split()]
        θ_nodes = [radians(90 - float(lat))\
                for lat in inf.readline().split()]
        r_nodes = [seispy.constants.EARTH_RADIUS - float(z)\
                for z in inf.readline().split()]
        φ_nodes = [φ - 2*π if φ > π else φ for φ in φ_nodes]
        R, T, P = np.meshgrid(r_nodes, θ_nodes, φ_nodes, indexing="ij")
        self.nodes = {"r": R, "θ": T, "φ": P}
        self.nodes["nr"] = R.shape[0]
        self.nodes["r_min"] = min(r_nodes)
        self.nodes["r_max"] = max(r_nodes)
        self.nodes["nθ"] = T.shape[1]
        self.nodes["θ_min"] = min(θ_nodes)
        self.nodes["θ_max"] = max(θ_nodes)
        self.nodes["nφ"] = P.shape[2]
        self.nodes["φ_min"] = min(φ_nodes)
        self.nodes["φ_max"] = max(φ_nodes)
        self.values = {"Vp": np.empty(shape=(len(r_nodes),
                                             len(θ_nodes),
                                             len(φ_nodes))),
                       "Vs": np.empty(shape=(len(r_nodes),
                                             len(θ_nodes),
                                             len(φ_nodes)))}
        for phase in "Vp", "Vs":
            for (ir, iθ) in [(ir, iθ) for ir in range(self.nodes["nr"])\
                    for iθ in range(self.nodes["nθ"])]:
                line = inf.readline().split()
                for iφ in range(len(line)):
                    self.values[phase][ir, iθ, iφ] = float(line[iφ])
        # Flip r and θ axis so they increase with increasing index.
        self.nodes["r"] = self.nodes["r"][::-1]
        self.nodes["θ"] = self.nodes["θ"][:,::-1]
        for phase in "Vp", "Vs":
            self.values[phase] = self.values[phase][::-1]
            self.values[phase] = self.values[phase][:,::-1]

    def _get_V(self, ρ, θ, φ, typeID, gridID):
        if isinstance(typeID, str):
            if typeID.upper() in ("P", "VP"):
                typeID = 1
            elif typeID.upper() in ("S", "VS"):
                typeID = 2
        model = self.v_type_grids[typeID][gridID]["data"]
        grid = self.v_type_grids[typeID][gridID]["grid"]

        iρ = (ρ - grid.ρ0)/grid.dρ
        iρ0 = min(max(int(np.floor(iρ)), 0), grid.nρ - 1)
        iρ1 = max(min(int(np.ceil(iρ)), grid.nρ - 1), 0)
        dρ = iρ - iρ0

        iθ = (θ - grid.θ0)/grid.dθ
        iθ0 = min(max(int(np.floor(iθ)), 0), grid.nθ - 1)
        iθ1 = max(min(int(np.ceil(iθ)), grid.nθ - 1), 0)
        dθ = iθ - iθ0
        #print(θ, iθ, iθ0, iθ1, grid.nθ)

        iφ = (φ - grid.φ0)/grid.dφ
        iφ0 = min(max(int(np.floor(iφ)), 0), grid.nφ - 1)
        iφ1 = max(min(int(np.ceil(iφ)), grid.nφ - 1), 0)
        dφ = iφ - iφ0

        V000 = model[iρ0,iθ0,iφ0]
        V001 = model[iρ0,iθ0,iφ1]
        V010 = model[iρ0,iθ1,iφ0]
        V011 = model[iρ0,iθ1,iφ1]
        V100 = model[iρ1,iθ0,iφ0]
        V101 = model[iρ1,iθ0,iφ1]
        V110 = model[iρ1,iθ1,iφ0]
        V111 = model[iρ1,iθ1,iφ1]

        V00 = V000 + (V100 - V000)*dρ
        V01 = V001 + (V101 - V001)*dρ
        V10 = V010 + (V110 - V010)*dρ
        V11 = V011 + (V111 - V011)*dρ

        V0 = V00 + (V10 - V00)*dθ
        V1 = V01 + (V11 - V01)*dθ

        V = V0 + (V1 - V0)*dφ

        return(V)

    def _get_V_dep(self, r, θ, φ, phase):
        """
        Return `phase` velocity at spherical coordinates (`r`, `θ`,
        `φ`).  Geographic coordinates can be converted to spherical
        coordinates using `seispy.geometry.geo2sph`.

        :param float r: Radial distance from coordinate system origin.
        :param float θ: Polar angle [0, pi].
        :param float φ: Azimuthal angle [0, 2*pi].
        :param str phase: Seismic phase ["P", "S", "Vp", "Vs"].
        """
        phase = _verify_phase(phase)
        # Make sure 0 <= φ < 2*pi
        φ %= 2 * pi
        φ -= 2 * pi
        if r > self.topo(*seispy.coords.as_spherical([r, θ, φ]).to_geographic()[:2]):
            # Return a null value if requested point is above surface.
            #return(-1)
            return(1)
        r = max(r, self.nodes["r_min"])
        θ = min(max(θ, self.nodes["θ_min"]),
                    self.nodes["θ_max"])
        φ = min(max(φ, self.nodes["φ_min"]),
                  self.nodes["φ_max"])
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

        θ_nodes = self.nodes["θ"][0,:,0]
        if θ <= θ_nodes[0]:
            iθ0 = 0
            dθ = 0
        elif θ >= θ_nodes[-1]:
            iθ0 = len(θ_nodes) - 1
            dθ = 0
        elif θ in θ_nodes:
            iθ0 = list(θ_nodes).index(θ)
            dθ = 0
        else:
            iθ0 = [True if cond(θ, b) else False for b in
                        zip(θ_nodes[:-1], θ_nodes[1:])].index(True)
            dθ = θ - θ_nodes[iθ0]

        φ_nodes = self.nodes["φ"][0,0,:]
        if φ <= φ_nodes[0]:
            iφ0 = 0
            dφ = 0
        elif φ >= φ_nodes[-1]:
            iφ0 = len(φ_nodes) - 1
            dφ = 0
        elif φ in φ_nodes:
            iφ0 = list(φ_nodes).index(φ)
            dφ = 0
        else:
            iφ0 = [True if cond(φ, b) else False for b in
                    zip(φ_nodes[:-1], φ_nodes[1:])].index(True)
            dφ = φ - φ_nodes[iφ0]
        ir1 = ir0 if ir0 == self.nodes["nr"] - 1 else ir0 + 1
        iθ1 = iθ0 if iθ0 == self.nodes["nθ"] - 1 else iθ0 + 1
        iφ1 = iφ0 if iφ0 == self.nodes["nφ"] - 1 else iφ0 + 1
        values = self.values[phase]
        V000, V100 = values[ir0, iθ0, iφ0], values[ir1, iθ0, iφ0]
        V010, V110 = values[ir0, iθ1, iφ0], values[ir1, iθ1, iφ0]
        V001, V101 = values[ir0, iθ0, iφ1], values[ir1, iθ0, iφ1]
        V011, V111 = values[ir0, iθ1, iφ1], values[ir1, iθ1, iφ1]
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
        if dθ == 0:
            V0, V1 = V00, V01
        else:
            V10 = V00 if V10 == -1 else V10
            V11 = V01 if V11 == -1 else V11
            dVdt = (V10 - V00) / (θ_nodes[iθ1] - θ_nodes[iθ0])
            V0 = V00 + dVdt * dθ / r
            dVdt = (V11 - V01) / (θ_nodes[iθ1] - θ_nodes[iθ0])
            V1 = V01 + dVdt * dθ / r
        if dφ == 0:
            V = V0
        else:
            V1 = V0 if V1 == -1 else V1
            dVdp = (V1 - V0) / (φ_nodes[iφ1] - φ_nodes[iφ0])
            V = V0 + dVdp * dφ / (r * np.sin(θ))
        return(V)

    def get_grid_center(self):
        """
        Return the center of the velocity model in spherical
        coordinates (r, θ, φ).

        :returns: coordinates of velocity model center in spherical
                  coordinates
        :rtype: (float, float, float)

        """
        return ((self.nodes["r_max"] + self.nodes["r_min"]) / 2,
                (self.nodes["θ_max"] + self.nodes["θ_min"]) / 2,
                (self.nodes["φ_max"] + self.nodes["φ_min"]) / 2)

    def regrid(self, R, T, P):
        Vp = np.empty(shape=R.shape)
        Vs = np.empty(shape=R.shape)
        for store, phase, index in ((Vp, "Vp", 0), (Vs, "Vs", 1)):
            for (ir, it, ip) in [(ir, it, ip) for ir in range(R.shape[0])
                                              for it in range(T.shape[1])
                                              for ip in range(P.shape[2])]:
                r, θ, φ = R[ir, it, ip], T[ir, it, ip], P[ir, it, ip]
                store[ir, it, ip] = self._get_V(r, θ, φ, phase)
        self.values["Vp"] = Vp
        self.values["Vs"] = Vs
        self.nodes["r"], self.nodes["θ"], self.nodes["φ"] = R, T, P
        self.nodes["nr"] = R.shape[0]
        self.nodes["nθ"] = T.shape[1]
        self.nodes["nφ"] = P.shape[2]
        self.nodes["dr"] = (R[:,0,0][-1] - R[:,0,0][0]) / (R.shape[0] - 1)
        self.nodes["dθ"] = (T[0,:,0][-1] - T[0,:,0][0]) / (T.shape[1] - 1)
        self.nodes["dφ"] = (P[0,0,:][-1] - P[0,0,:][0]) / (P.shape[2] - 1)
        self.nodes["r_min"], self.nodes["r_max"] = np.min(R), np.max(R)
        self.nodes["θ_min"], self.nodes["θ_max"] = np.min(T), np.max(T)
        self.nodes["φ_min"], self.nodes["φ_max"] = np.min(P), np.max(P)

    def regularize(self, nr, nθ, nφ):
        R, T, P = np.meshgrid(np.linspace(self.nodes["r_min"],
                                          self.nodes["r_max"],
                                          nr),
                              np.linspace(self.nodes["θ_min"],
                                          self.nodes["θ_max"],
                                          nθ),
                              np.linspace(self.nodes["φ_min"],
                                          self.nodes["φ_max"],
                                          nφ),
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
    vm = VelocityModel("/Users/malcolcw/Projects/Wavefront/examples/example2/vgrids.in", "fmm3d")
    grid = vm.v_type_grids[1][1]["grid"]
    print(vm(1, 3, 0.5, 0.5, 0))
    #vm.v_type_grids[1][1]
    #print(v("Vp", 33.0, -116.9, 3.0))

if __name__ == "__main__":
    test()
    print("velocity.py is not an executable script.")
    exit()
