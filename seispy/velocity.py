# coding=utf-8
from math import degrees,\
                 pi,\
                 radians
import numpy as np
import pandas as pd
import scipy.interpolate

from . import constants as _constants
from . import coords as _coords
from . import geometry as _geometry


class VelocityModel(object):
    def __init__(self, inf=None, fmt=None, topo=None, **kwargs):
        """
        A callable class providing a queryable container for seismic
        velocities in a 3D volume.

        :param str inf: path to input file containing phase velocity
                           data
        :param str fmt: format of input file
        """
        if inf is None:
            return
        if topo is None:
            self.topo = lambda _, __: _constants.EARTH_RADIUS
        else:
            self.topo = topo

        if fmt.upper() == "FANG":
            self._read_fang(inf, **kwargs)
        elif fmt.upper() in ("FM3D", "FMM3D"):
            raise(NotImplementedError(f"Unrecognized format - {fmt}"))
            self._read_fmm3d(inf, **kwargs)
        elif fmt.upper() in ("UCVM", "SCEC-UCVM"):
            self._read_ucvm(inf, **kwargs)
        elif fmt.upper() == "NPZ":
            self._read_npz(inf)
        else:
            raise(ValueError(f"Unrecognized format - {fmt}"))

    def from_DataFrame(self, df):
        df["R"] = df["T"] = df["P"] = np.nan
        spher = _coords.as_geographic(df[["lat", "lon", "depth"]]
                                           ).to_spherical()
        df.loc[:, ["R", "T", "P"]] = spher
        df = df.sort_values(["R", "T", "P"])
        nR = len(df.drop_duplicates("R"))
        nT = len(df.drop_duplicates("T"))
        nP = len(df.drop_duplicates("P"))
        nodes = df[["R", "T", "P"]].values.reshape(nR, nT, nP, 3)
        self._nodes = _coords.as_spherical(nodes)
        Vp = df["Vp"].values.reshape(nR, nT, nP)
        Vs = df["Vs"].values.reshape(nR, nT, nP)
        self._Vp = Vp
        self._Vs = Vs
        return(self)

    def to_DataFrame(self):
        df = pd.DataFrame().from_dict({"R": self._nodes[...,0].flatten(),
                                       "T": self._nodes[...,1].flatten(),
                                       "P": self._nodes[...,2].flatten(),
                                       "Vp": self._Vp.flatten(),
                                       "Vs": self._Vs.flatten()})
        df["lat"] = df["lon"] = df["depth"] = np.nan
        geo = _coords.as_spherical(df[["R", "T", "P"]]).to_geographic()
        df.loc[:, ["lat", "lon", "depth"]] = geo
        df = df.sort_values(["lat", "lon", "depth"]).reset_index()
        return(df[["lat", "lon", "depth", "Vp", "Vs", "R", "T", "P"]])

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

        rho, theta, phi = _coords.as_geographic([lat, lon, depth]).to_spherical()
        return(self._get_V(phase, rho, theta, phi))

    def save(self, outf):
        np.savez(outf, nodes=self._nodes, Vp=self._Vp, Vs=self._Vs)

    def _read_npz(self, inf):
        inf = np.load(inf)
        self._nodes = _coords.as_spherical(inf["nodes"])
        self._Vp = inf["Vp"]
        self._Vs = inf["Vs"]

    def _read_ucvm(self, inf, Vp_key="cmb_vp", Vs_key="cmb_vs"):
        names=["lon", "lat", "Z", "surf", "vs30", "crustal", "cr_vp", "cr_vs",
               "cr_rho", "gtl", "gtl_vp", "gtl_vs", "gtl_rho", "cmb_algo",
               "cmb_vp", "cmb_vs", "cmb_rho"]
        df = pd.read_table(inf,
                      delim_whitespace=True,
                      header=None,
                      names=names)
        df["depth"] = df["Z"]*1e-3
        df["Vp"] = df[Vp_key]*1e-3
        df["Vs"] = df[Vs_key]*1e-3
        df["R"] = df["T"] = df["P"] = np.nan
        spher = _coords.as_geographic(df[["lat", "lon", "depth"]]
                                           ).to_spherical()
        df.loc[:, ["R", "T", "P"]] = spher
        df = df.sort_values(["R", "T", "P"])
        nR = len(df.drop_duplicates("R"))
        nT = len(df.drop_duplicates("T"))
        nP = len(df.drop_duplicates("P"))
        nodes = df[["R", "T", "P"]].values.reshape(nR, nT, nP, 3)
        self._nodes = _coords.as_spherical(nodes)
        Vp = df["Vp"].values.reshape(nR, nT, nP)
        Vs = df["Vs"].values.reshape(nR, nT, nP)
        self._Vp = Vp
        self._Vs = Vs

    def _read_fang(self, inf):
        with open(inf) as inf:
            lon = np.array([float(v) for v in inf.readline().split()])
            lat = np.array([float(v) for v in inf.readline().split()])
            depth = np.array([float(v) for v in inf.readline().split()])
            LAT, LON, DEPTH = np.meshgrid(lat, lon, depth, indexing="ij")
            VVp = np.zeros(LAT.shape)
            VVs = np.zeros(LAT.shape)
            for idepth in range(len(depth)):
                for ilat in range(len(lat)):
                    VVp[ilat, :, idepth] = np.array([float(v) for v in inf.readline().split()])
            for idepth in range(len(depth)):
                for ilat in range(len(lat)):
                    VVs[ilat, :, idepth] = np.array([float(v) for v in inf.readline().split()])
        spher = _coords.as_geographic(np.stack([LAT.flatten(),
                                                      LON.flatten(),
                                                      DEPTH.flatten()],
                                                     axis=1)
                                           ).to_spherical()
        df = pd.DataFrame.from_dict({"R": spher[:,0],
                                     "T": spher[:,1],
                                     "P": spher[:,2],
                                     "Vp": VVp.flatten(),
                                     "Vs": VVs.flatten()})
        df = df.sort_values(["R", "T", "P"])
        nR = len(df.drop_duplicates("R"))
        nT = len(df.drop_duplicates("T"))
        nP = len(df.drop_duplicates("P"))
        self._nodes = df[["R", "T", "P"]].values.reshape(nR, nT, nP, 3)
        Vp = df["Vp"].values.reshape(nR, nT, nP)
        Vs = df["Vs"].values.reshape(nR, nT, nP)
        self._Vp = Vp
        self._Vs = Vs

    def _get_V(self, phase: str, rho: float, theta: float, phi: float)->float:
        phase = _verify_phase(phase)
        if phase == "P":
            VV = self._Vp
        elif phase == "S":
            VV = self._Vs
        else:
            raise(ValueError(f"Unrecognized phase type: {phase}"))


        idx = np.nonzero(self._nodes[:,0,0,0] == rho)[0]
        if idx.size > 0:
            iR0, iR1 = idx[0], idx[0]
        else:
            idxl = np.nonzero(self._nodes[:,0,0,0] < rho)[0]
            idxr = np.nonzero(self._nodes[:,0,0,0] > rho)[0]
            if not np.any(idxl):
                iR0, iR1 = 0, 0
            elif not np.any(idxr):
                iR0, iR1 = -1, -1
            else:
                iR0, iR1 = idxl[-1], idxr[0]
        if iR0 == iR1:
            dR, drho = 1, 0
        else:
            dR = self._nodes[iR1,0,0,0]-self._nodes[iR0,0,0,0]
            drho = (rho - self._nodes[iR0,0,0,0])


        idx = np.nonzero(self._nodes[0,:,0,1] == theta)[0]
        if idx.size > 0:
            iT0, iT1 = idx[0], idx[0]
        else:
            idxl = np.nonzero(self._nodes[0,:,0,1] < theta)[0]
            idxr = np.nonzero(self._nodes[0,:,0,1] > theta)[0]
            if not np.any(idxl):
                iT0, iT1 = 0, 0
            elif not np.any(idxr):
                iT0, iT1 = -1, -1
            else:
                iT0, iT1 = idxl[-1], idxr[0]
        if iT0 == iT1:
            dT, dtheta = 1, 0
        else:
            dT = self._nodes[0,iT1,0,1]-self._nodes[0,iT0,0,1]
            dtheta = (theta - self._nodes[0,iT0,0,1])


        idx = np.nonzero(self._nodes[0,0,:,2] == phi)[0]
        if idx.size > 0:
            iP0, iP1 = idx[0], idx[0]
        else:
            idxl = np.nonzero(self._nodes[0,0,:,2] < phi)[0]
            idxr = np.nonzero(self._nodes[0,0,:,2] > phi)[0]
            if not np.any(idxl):
                iP0, iP1 = 0, 0
            elif not np.any(idxr):
                iP0, iP1 = -1, -1
            else:
                iP0, iP1 = idxl[-1], idxr[0]
        if iP0 == iP1:
            dP, dphi = 1, 0
        else:
            dP = self._nodes[0,0,iP1,2]-self._nodes[0,0,iP0,2]
            dphi = (phi - self._nodes[0,0,iP0,2])


        V000 = VV[iR0,iT0,iP0]
        V001 = VV[iR0,iT0,iP1]
        V010 = VV[iR0,iT1,iP0]
        V011 = VV[iR0,iT1,iP1]
        V100 = VV[iR1,iT0,iP0]
        V101 = VV[iR1,iT0,iP1]
        V110 = VV[iR1,iT1,iP0]
        V111 = VV[iR1,iT1,iP1]

        V00 = V000 + (V100 - V000)*drho/dR
        V01 = V001 + (V101 - V001)*drho/dR
        V10 = V010 + (V110 - V010)*drho/dR
        V11 = V011 + (V111 - V011)*drho/dR

        V0 = V00 + (V10 - V00)*dtheta/dT
        V1 = V01 + (V11 - V01)*dtheta/dT

        V = V0 + (V1 - V0)*dphi/dP

        return(V)

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

        (lon1, lat1), (lon2, lat2) = _geometry.get_line_endpoints(lat0,
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
                X[i, j] = _geometry.distance((lat1, lon1), (lat, lon))
                Y[i, j] = depth
        V = np.ma.masked_equal(V, -1)
        return(X, Y, V)

def _verify_phase(phase: str)->str:
    if phase.upper() == "P" or  phase.upper() == "VP":
        phase = "P"
    elif phase.upper() == "S" or phase.upper() == "VS":
        phase = "S"
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
