# coding=utf-8
"""
This module facilitates access to velocity model data.

.. todo::
   Make a ScalarField class to abstract behaviour in this class.

.. autoclass:: VelocityModel
   :special-members:
   :private-members:
   :members:
"""
# The next line sets the tolerance, in decimal places, for comparing float equivalence 
_TOLERANCE = 12

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from collections import deque

from . import constants as _constants
from . import coords as _coords
from . import geometry as _geometry
from . import mapping as _mapping

_PI = np.pi


class VelocityModel(object):
    """
    A callable class providing a queryable container for seismic
    velocities in a 3D volume.

    :param str inf: path to input file containing phase velocity
                    data
    :param str fmt: format of input file
    :attr bool _is_regular: is grid regular
    :attr float rho0: rho coordinate of grid origin, None if grid is irregular
    :attr float theta0: theta coordinate of grid origin, None if grid is irregular
    :attr float phi0: phi coordinate of grid origin, None if grid is irregular
    :attr float drho: grid node interval in rho direction, None if grid is irregular
    :attr float dtheta: grid node interval in theta direction, None if grid is irregular
    :attr float dphi: grid node interval in phi direction, None if grid is irregular
    :attr int nrho: number of grid nodes in rho direction, None if grid is irregular
    :attr int ntheta: number of grid nodes in theta direction, None if grid is irregular
    :attr int nphi: number of grid nodes in phi direction, None if grid is irregular
    
    Data are always stored internally using a spherical coordinate system. The client
    must account for this when working with the data directly.
    
    NOTE:: the topo attribute is causing pickling errors due to use of locally defined
    lambda functionand isn't used for anything right now
    """
    def __init__(self, inf=None, fmt=None, topo=None, **kwargs):
        self._inf, self._fmt, self._topo = inf, fmt, topo
        self._is_regular = False
        self._rho0, self._theta0, self._phi0 = None, None, None
        self._drho, self._dtheta, self._dphi = None, None, None
        self._nrho, self._ntheta, self._nphi = None, None, None
        if inf is None:
            return
        #if topo is None:
        #    self.topo = lambda _, __: _constants.EARTH_RADIUS
        #else:
        #    self.topo = topo
        if fmt.upper() == "FANG":
            self._read_fang(inf, **kwargs)
        elif fmt.upper() in ("FM3D", "FMM3D"):
            self._read_fm3d(inf, **kwargs)
        elif fmt.upper() in ("ABZ", "ABZ2014", "ABZ14"):
            self._read_abz(inf, **kwargs)
        elif fmt.upper() in ("UCVM", "SCEC-UCVM"):
            self._read_ucvm(inf, **kwargs)
        elif fmt.upper() == "NPZ":
            self._read_npz(inf)
        else:
            raise(ValueError(f"Unrecognized format - {fmt.upper()}"))


    @property
    def bounds(self):
        rmin = float(self.nodes[..., 0].min())
        rmax = float(self.nodes[..., 0].max())
        tmin = float(self.nodes[..., 1].min())
        tmax = float(self.nodes[..., 1].max())
        pmin = float(self.nodes[..., 2].min())
        pmax = float(self.nodes[..., 2].max())
        return ((rmin, rmax), (tmin, tmax), (pmin, pmax))

    
    @property
    def nodes(self):
        return(self._nodes)


    @nodes.setter
    def nodes(self, value):
        if not isinstance(value, _coords.SphericalCoordinates):
            try:
                value = value.to_spherical()
            except:
                raise (TypeError('Sorry! I couldn\'t understand the coordinate system I received.'))
        interval = lambda iterable: np.unique(
            np.round(np.diff(np.unique(iterable)), _TOLERANCE)
        )
        if interval(value[..., 0]).shape == (1,) \
                and interval(value[..., 1]).shape == (1,) \
                and interval(value[..., 2]).shape == (1,):
            self._is_regular = True
            self.rho0       = value[..., 0].min()
            self.theta0     = value[..., 1].min()
            self.phi0       = value[..., 2].min()
            self.drho       = interval(value[..., 0])[0]
            self.dtheta     = interval(value[..., 1])[0]
            self.dphi       = interval(value[..., 2])[0]
            self.nrho, self.ntheta, self.nphi = value.shape[:3]
        self._vp = self('p', value.to_geographic())
        self._vs = self('s', value.to_geographic())
        self._nodes = value


    @property
    def rho0(self):
        return (self._rho0)


    @rho0.setter
    def rho0(self, value):
        self._rho0 = value
    

    @property
    def theta0(self):
        return (self._theta0)
    

    @theta0.setter
    def theta0(self, value):
        self._theta0 = value


    @property
    def lambda0(self):
        return (_PI / 2 - (self.theta0 + (self.ntheta - 1) * self.dtheta))

    
    @lambda0.setter
    def lambda0(self, value):
        raise (NotImplementedError('sorry, lambda0 is an immutable attribute'))


    @property
    def phi0(self):
        return (self._phi0)


    @phi0.setter
    def phi0(self, value):
        self._phi0 = value


    @property
    def lat0(self):
        return (np.degrees(self.lambda0))


    @lat0.setter
    def lat0(self, value):
        raise (NotImplementedError('sorry, lat0 is an immutable attribute'))


    @property
    def lon0(self):
        return (np.degrees(self.phi0))


    @lon0.setter
    def lon(self, value):
        raise (NotImplementedError('sorry, lon0 is an immutable attribute'))


    @property
    def depth0(self):
        return (_constants.EARTH_RADIUS - (self.rho0 + (self.nrho - 1) * self.drho))


    @depth0.setter
    def depth0(self, value):
        raise (NotImplementedError('sorry, depth0 is an immutable attribute'))


    @property
    def drho(self):
        return (self._drho)


    @drho.setter
    def drho(self, value):
        self._drho = value


    @property
    def dtheta(self):
        return (self._dtheta)


    @dtheta.setter
    def dtheta(self, value):
        self._dtheta = value


    @property
    def dlambda(self):
        return (self._dtheta)


    @dlambda.setter
    def dlambda(self, value):
        raise (NotImplementedError('sorry, dlambda is an immutable attribute'))


    @property
    def dphi(self):
        return( self._dphi)


    @dphi.setter
    def dphi(self, value):
        self._dphi = value


    @property
    def dlat(self):
        return (np.degrees(self.dtheta))


    @dlat.setter
    def dlat(self, value):
        raise (NotImplementedError('sorry, dlat is an immutable attribute'))


    @property
    def dlon(self):
        return (np.degrees(self.dphi))


    @dlon.setter
    def dlon(self, value):
        raise (NotImplementedError('sorry, dlon is an immutable attribute'))


    @property
    def ddepth(self):
        return (self.drho)


    @ddepth.setter
    def ddepth(self, value):
        raise (NotImplementedError('sorry, ddepth is an immutable attribute'))


    @property
    def nrho(self):
        return( self._nrho)


    @nrho.setter
    def nrho(self, value):
        self._nrho = value


    @property
    def ntheta(self):
        return( self._ntheta)


    @ntheta.setter
    def ntheta(self, value):
        self._ntheta = value


    @property
    def nlambda(self):
        return (self._ntheta)


    @nlambda.setter
    def nlambda(self, value):
        raise (NotImplementedError('sorry, nlambda is an immutable attribute'))


    @property
    def nphi(self):
        return( self._nphi)


    @nphi.setter
    def nphi(self, value):
        self._nphi = value


    @property
    def nlat(self):
        return (self._ntheta)


    @nlat.setter
    def nlat(self, value):
        raise (NotImplementedError('sorry, nlat is an immutable attribute'))


    @property
    def nlon(self):
        return (self._nphi)


    @nlon.setter
    def nlon(self, value):
        raise (NotImplementedError('sorry, nlon is an immutable attribute'))


    @property
    def ndepth(self):
        return (self._nrho)


    @ndepth.setter
    def ndepth(self, value):
        raise (NotImplementedError('sorry, ndepth is an immutable attribute'))


    def from_DataFrame(self, df):
        '''
        TODO:: This method does not conform to class standards.
        
        Initialize VelocityModel from a pandas.DataFrame. Input
        DataFrame must have *lat*, *lon*, *depth*, *vp*, and *vs*,
        fields.

        :param pandas.DataFrame df: DataFrame with velocity data
        '''
        df["R"] = df["T"] = df["P"] = np.nan
        spher = _coords.as_geographic(df[["lat", "lon", "depth"]]
                                           ).to_spherical()
        df.loc[:, ["R", "T", "P"]] = spher
        df = df.sort_values(["R", "T", "P"])
        nR = len(df.drop_duplicates("R"))
        nT = len(df.drop_duplicates("T"))
        nP = len(df.drop_duplicates("P"))
        nodes = df[["R", "T", "P"]].values.reshape(nR, nT, nP, 3)
        dr = np.unique(np.round(np.diff(np.unique(nodes[..., 0].flatten())), 9))
        dt = np.unique(np.round(np.diff(np.unique(nodes[..., 1].flatten())), 9))
        dp = np.unique(np.round(np.diff(np.unique(nodes[..., 2].flatten())), 9))
        if len(dr) == len(dt) == len(dp) == 1:
            self._is_regular = True
            self._dr, self._dt, self._dp = dr[0], dt[0], dp[0]
            self._nR, self._nT, self._nP = nR, nT, nP
            self._R0 = nodes[..., 0].min()
            self._T0 = nodes[..., 1].min()
            self._L0 = np.pi/2 - nodes[..., 1].max()
            self._P0 = nodes[..., 2].min()
        self._nodes = _coords.as_spherical(nodes)
        vp = df["vp"].values.reshape(nR, nT, nP)
        vs = df["vs"].values.reshape(nR, nT, nP)
        self._vp = vp
        self._vs = vs
        return(self)

    def to_DataFrame(self):
        df = pd.DataFrame().from_dict({"R": self._nodes[...,0].flatten(),
                                       "T": self._nodes[...,1].flatten(),
                                       "P": self._nodes[...,2].flatten(),
                                       "vp": self._vp.flatten(),
                                       "vs": self._vs.flatten()})
        df["lat"] = df["lon"] = df["depth"] = np.nan
        geo = _coords.as_spherical(df[["R", "T", "P"]]).to_geographic()
        df.loc[:, ["lat", "lon", "depth"]] = geo
        df = df.sort_values(["lat", "lon", "depth"]).reset_index()
        return(df[["lat", "lon", "depth", "vp", "vs", "R", "T", "P"]])

    def __call__(self, phase, coords):
        """
        Return **phase**-velocity at given coordinates. A NULL value
        (-1) is returned for points above the surface.

        :param str phase: phase
        :param array-like coords: coordinates
        :returns: **phase**-velocity at coordinates
        :rtype: array-like
        """
        # Convert geographic coordinates to spherical
        rtp = _coords.as_geographic(coords).to_spherical()
        def func(coords):
            v = self._get_V(phase, *coords)
            return (self._get_V(phase, *coords))
        vv = np.array(list(map(func, rtp.reshape(-1, 3)))).reshape(rtp.shape[:-1])
        return(vv)


    def __str__(self)->str:
        s = 'seispy.velocity.VelocityModel object\n'
        s += f'    inf:  {self._inf}\n'
        s += f'    fmt:  {self._fmt.upper() if self._fmt is not None else None}\n'
        #s += f'    topo: {self._topo.upper() if self._topo is not None else None}\n'
        return(s)


    def save(self, outf):
        np.savez(
            outf,
            nodes=self._nodes, vp=self._vp, vs=self._vs,
            is_regular=self._is_regular,
            grid_parameters=[
                self.rho0, self.theta0, self.phi0,
                self.drho, self.dtheta, self.dphi,
                self.nrho, self.ntheta, self.nphi
            ]
        )

    def _read_npz(self, inf):
        inf = np.load(inf)
        self._nodes = _coords.as_spherical(inf["nodes"])
        self._vp = inf["vp"]
        self._vs = inf["vs"]
        self._is_regular = inf['is_regular']
        if self._is_regular:
            grid_params = inf['grid_parameters']
            self.rho0, self.theta0, self.phi0 = grid_params[ :3]
            self.drho, self.dtheta, self.dphi = grid_params[3:6]
            self.nrho, self.ntheta, self.nphi = [int(v) for v in grid_params[6: ]]
        else:
            self.rho0, self.theta0, self.phi0 = None, None, None 
            self.drho, self.dtheta, self.dphi = None, None, None 
            self.nrho, self.ntheta, self.nphi = None, None, None 

    def _read_ucvm(self, inf, vp_key="cmb_vp", vs_key="cmb_vs"):
        names=["lon", "lat", "Z", "surf", "vs30", "crustal", "cr_vp", "cr_vs",
               "cr_rho", "gtl", "gtl_vp", "gtl_vs", "gtl_rho", "cmb_algo",
               "cmb_vp", "cmb_vs", "cmb_rho"]
        df = pd.read_table(inf,
                      delim_whitespace=True,
                      header=None,
                      names=names)
        df["depth"] = df["Z"]*1e-3
        df["vp"] = df[vp_key]*1e-3
        df["vs"] = df[vs_key]*1e-3
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
        vp = df["vp"].values.reshape(nR, nT, nP)
        vs = df["vs"].values.reshape(nR, nT, nP)
        self._vp = vp
        self._vs = vs

    def _read_abz(self, inf, **kwargs):
        df = pd.read_table(inf,
                           header=None,
                           delim_whitespace=True,
                           names=["lat", "lon", "depth", "vp", "vs", "DWS"])
        self.from_DataFrame(df)
        return(self)

    def _read_fang(self, inf):
        with open(inf) as inf:
            lon = np.array([float(v) for v in inf.readline().split()])
            lat = np.array([float(v) for v in inf.readline().split()])
            depth = np.array([float(v) for v in inf.readline().split()])
            LAT, LON, DEPTH = np.meshgrid(lat, lon, depth, indexing="ij")
            vvp = np.zeros(LAT.shape)
            vvs = np.zeros(LAT.shape)
            for idepth in range(len(depth)):
                for ilat in range(len(lat)):
                    vvp[ilat, :, idepth] = np.array([float(v) for v in inf.readline().split()])
            for idepth in range(len(depth)):
                for ilat in range(len(lat)):
                    vvs[ilat, :, idepth] = np.array([float(v) for v in inf.readline().split()])
        spher = _coords.as_geographic(np.stack([LAT.flatten(),
                                                      LON.flatten(),
                                                      DEPTH.flatten()],
                                                     axis=1)
                                           ).to_spherical()
        df = pd.DataFrame.from_dict({"R": spher[:, 0],
                                     "T": spher[:, 1],
                                     "P": spher[:, 2],
                                     "vp": vvp.flatten(),
                                     "vs": vvs.flatten()})
        df = df.sort_values(["R", "T", "P"])
        nR = len(df.drop_duplicates("R"))
        nT = len(df.drop_duplicates("T"))
        nP = len(df.drop_duplicates("P"))
        self._nodes = df[["R", "T", "P"]].values.reshape(nR, nT, nP, 3)
        vp = df["vp"].values.reshape(nR, nT, nP)
        vs = df["vs"].values.reshape(nR, nT, nP)
        self._vp = vp
        self._vs = vs

    def _read_fm3d(self, inf: str):
        self._is_regular = True
        with open(inf, 'r') as inf:
            data = deque(inf.read().split('\n'))
        nvgrids, nvtypes = (int(v) for v in data.popleft().split())
        nr, nlamda, nphi = (int(v) for v in data.popleft().split())
        dr, dlamda, dphi = (float(v) for v in data.popleft().split())
        r0, lamda0, phi0 = (float(v) for v in data.popleft().split())
        nnp = nr * nlamda * nphi
        vp = np.array([float(data.popleft()) for i in range(nnp)])
        nr, nlamda, nphi = (int(v) for v in data.popleft().split())
        dr, dlamda, dphi = (float(v) for v in data.popleft().split())
        r0, lamda0, phi0 = (float(v) for v in data.popleft().split())
        nns = nr * nlamda * nphi
        vs = np.array([float(data.popleft()) for i in range(nns)])
        r_nodes = np.array([r0 + i * dr for i in range(nr)])
        t_nodes = np.array([np.pi/2-(lamda0 + i * dlamda)
                            for i in range(nlamda)])
        p_nodes = np.array([phi0 + i * dphi for i in range(nphi)])
        r_mesh, t_mesh, p_mesh = np.meshgrid(r_nodes,
                                             t_nodes,
                                             p_nodes,
                                             indexing='ij')
        spher = _coords.as_spherical(np.stack([r_mesh.flatten(),
                                               t_mesh.flatten(),
                                               p_mesh.flatten()],
                                               axis=1))
        geo = spher.to_geographic()
        df = pd.DataFrame({'lat': geo[:, 0],
                            'lon': geo[:, 1],
                            'depth': geo[:, 2],
                            'vp': vp,
                            'vs': vs})
        self.from_DataFrame(df)
        return(self)

    def _get_V(self, phase: str, rho: float, theta: float, phi: float)->float:
        phase = _verify_phase(phase)
        if phase == "P":
            VV = self._vp
        elif phase == "S":
            VV = self._vs
        else:
            raise(ValueError(f"Unrecognized phase type: {phase}"))


        idx = np.nonzero(self._nodes[:, 0, 0, 0] == rho)[0]
        if idx.size > 0:
            iR0, iR1 = idx[0], idx[0]
        else:
            idxl = np.nonzero(self._nodes[:, 0, 0, 0] < rho)[0]
            idxr = np.nonzero(self._nodes[:, 0, 0, 0] > rho)[0]
            if not np.any(idxl):
                iR0, iR1 = 0, 0
            elif not np.any(idxr):
                iR0, iR1 = -1, -1
            else:
                iR0, iR1 = idxl[-1], idxr[0]
        if iR0 == iR1:
            dr, drho = 1, 0
        else:
            dr = self._nodes[iR1, 0, 0, 0]-self._nodes[iR0, 0, 0, 0]
            drho = (rho - self._nodes[iR0, 0, 0, 0])


        idx = np.nonzero(self._nodes[0, :, 0, 1] == theta)[0]
        if idx.size > 0:
            iT0, iT1 = idx[0], idx[0]
        else:
            idxl = np.nonzero(self._nodes[0, :, 0, 1] < theta)[0]
            idxr = np.nonzero(self._nodes[0, :, 0, 1] > theta)[0]
            if not np.any(idxl):
                iT0, iT1 = 0, 0
            elif not np.any(idxr):
                iT0, iT1 = -1, -1
            else:
                iT0, iT1 = idxl[-1], idxr[0]
        if iT0 == iT1:
            dt, dtheta = 1, 0
        else:
            dt = self._nodes[0, iT1, 0, 1]-self._nodes[0, iT0, 0, 1]
            dtheta = (theta - self._nodes[0, iT0, 0, 1])


        idx = np.nonzero(self._nodes[0, 0, :, 2] == phi)[0]
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
            dp, dphi = 1, 0
        else:
            dp = self._nodes[0,0,iP1,2]-self._nodes[0,0,iP0,2]
            dphi = (phi - self._nodes[0,0,iP0,2])

        V000 = VV[iR0,iT0,iP0]
        V001 = VV[iR0,iT0,iP1]
        V010 = VV[iR0,iT1,iP0]
        V011 = VV[iR0,iT1,iP1]
        V100 = VV[iR1,iT0,iP0]
        V101 = VV[iR1,iT0,iP1]
        V110 = VV[iR1,iT1,iP0]
        V111 = VV[iR1,iT1,iP1]

        V00 = V000 + (V100 - V000)*drho/dr
        V01 = V001 + (V101 - V001)*drho/dr
        V10 = V010 + (V110 - V010)*drho/dr
        V11 = V011 + (V111 - V011)*drho/dr

        V0 = V00 + (V10 - V00)*dtheta/dt
        V1 = V01 + (V11 - V01)*dtheta/dt

        V = V0 + (V1 - V0)*dphi/dp

        return (V)


    def get_center(self):
        r0 = (self._nodes[..., 0].min() + self._nodes[..., 0].max()) / 2
        t0 = (self._nodes[..., 1].min() + self._nodes[..., 1].max()) / 2
        p0 = (self._nodes[..., 2].min() + self._nodes[..., 2].max()) / 2
        return (_coords.as_spherical((r0, t0, p0)))


    def pad(self, nrho=0, ntheta=0, nphi=0):
        bounds = self.bounds
        rho_min, rho_max     = bounds[0]
        theta_min, theta_max = bounds[1]
        phi_min, phi_max     = bounds[2]
        rho = np.linspace(
            rho_min + min(nrho, 0) * self.drho,
            rho_max + max(nrho, 0) * self.drho,
            self.nrho + abs(nrho)
        )
        theta = np.linspace(
            theta_min + min(ntheta, 0) * self.dtheta,
            theta_max + max(ntheta, 0) * self.dtheta,
            self.ntheta + abs(ntheta)
        )
        phi = np.linspace(
            phi_min + min(nphi, 0) * self.dphi,
            phi_max + max(nphi, 0) * self.dphi,
            self.nphi + abs(nphi)
        )
        self.nodes = _coords.as_spherical(
            np.stack(
                np.meshgrid(rho, theta, phi, indexing="ij"),
                axis=-1
            )
        )


    def regularize(self, nr, ntheta, nphi):
        bounds = self.bounds
        rho_min, rho_max     = bounds[0]
        theta_min, theta_max = bounds[1]
        phi_min, phi_max     = bounds[2]
        self.nodes = _coords.as_spherical(
            np.stack(
                np.meshgrid(
                    np.linspace(rho_min, rho_max, nr),
                    np.linspace(theta_min, theta_max, ntheta),
                    np.linspace(phi_min, phi_max, nphi),
                    indexing="ij"
                ),
                axis=-1
            )
        )

    def extract_slice(self, phase="P", origin=(33.5, -116.5, 0), strike=0,
                      length=50, zmin=0, zmax=25, nx=25, nz=25):
        r"""
        Extract an arbitrarily oriented vertical slice from the VelocityModel.
        """
        n = np.linspace(-length, length, nx)
        d = np.linspace(zmin, zmax, nz)
        nn, dd = np.meshgrid(n, d)
        ee = np.zeros(nn.shape)
        ned = _coords.as_ned(np.stack([nn, ee, dd], axis=2))
        ned.set_origin(origin)
        geo = ned.to_geographic()
        vv = self(phase, geo)
        # vv = self("vp", geo)/self("vs", geo)
        return (vv, ned, geo)

    def plot(self, phase="P", ix=None, iy=None, iz=None, type="fancy",
             events=None, faults=False, vmin=None, vmax=None,
             basemap_kwargs=None):
        r"""
        This needs to be cleaned up, but it will plot a velocity model
        (map-view) and two perendicular, user-selected vertical slices.
        """
        phase = _verify_phase(phase)
        if phase == "P":
            data = self._vp
        elif phase == "S":
            data = self._vs
        ix = int((self._nodes.shape[2]-1)/2) if ix is None else ix
        iy = int((self._nodes.shape[1]-1)/2) if iy is None else iy
        iz = -1 if iz is None else iz
        vmin = data.min() if vmin is None else vmin
        vmax = data.max() if vmax is None else vmax
        basemap_kwargs = {} if basemap_kwargs is None else basemap_kwargs
        origin = self._nodes.to_geographic()[iz, iy, ix]
        if events is not None:
            events = seispy.coords.as_geographic(events[["lat", "lon", "depth"]])
        fig = plt.figure(figsize=(11,8.5))
        ax0 = fig.add_axes((0.05, 0.3, 0.7, 0.65))
        nodes = self._nodes.to_geographic()
        _basemap_kwargs = dict(llcrnrlat=nodes[..., 0].min(),
                               llcrnrlon=nodes[..., 1].min(),
                               urcrnrlat=nodes[..., 0].max(),
                               urcrnrlon=nodes[..., 1].max())
        basemap_kwargs = {**_basemap_kwargs, **basemap_kwargs}
        bm = _mapping.Basemap(basekwargs=basemap_kwargs,
                              ax=ax0,
                              meridian_labels=[False, False, True, False])
        qmesh = bm.overlay_pcolormesh(nodes[iz, ..., 1].flatten(),
                                      nodes[iz, ..., 0].flatten(),
                                      data[iz].flatten(),
                                      cmap=plt.get_cmap("jet_r"),
                                      vmin=vmin,
                                      vmax=vmax)
        if faults is True:
            bm.add_faults()
        if events is not None:
            bm.scatter(events[:,1], events[:,0], 
                       c="k",
                       s=0.1,
                       linewidths=0, 
                       zorder=3,
                       alpha=0.25)
        (xmin, ymin), (xmax, ymax) = bm.ax.get_position().get_points()
        cax = fig.add_axes((0.9, ymin, 0.025, ymax - ymin))
        cbar = fig.colorbar(qmesh, cax=cax)
        cbar.ax.invert_yaxis()
        cbar.set_label(f"$V_{phase.lower()}$ "+r"[$\frac{km}{s}$]")
        # Plot the NS vertical slice
        bm.axvline(x=origin[1], zorder=3, linestyle="--", color="k")
        ax_right = fig.add_axes((xmax, ymin, 1-xmax, ymax-ymin))
        ned = self._nodes[:, :, ix].to_ned(origin=origin)
        ax_right.pcolormesh(ned[..., 2], ned[..., 0], data[:, :, ix],
                            cmap=plt.get_cmap("jet_r"),
                            vmin=vmin,
                            vmax=vmax)
        
        ax_right.set_aspect(1)
        ax_right.yaxis.tick_right()
        ax_right.yaxis.set_label_position("right")
        ax_right.set_xlabel("[$km$]", rotation=180)
        ax_right.set_ylabel("[$km$]")
        ax_right.tick_params(axis="y", labelrotation=90)
        ax_right.tick_params(axis="x", labelrotation=90)
        # Plot the EW vertical slice
        bm.axhline(y=origin[0], zorder=3, linestyle="--", color="k")
        ax_bottom = fig.add_axes((xmin, 0, xmax-xmin, ymin))
        ned = self._nodes[:, iy, :].to_ned(origin=origin)
        ax_bottom.pcolormesh(ned[..., 1], ned[..., 2], data[:, iy, :],
                             cmap=plt.get_cmap("jet_r"),
                             vmin=vmin,
                             vmax=vmax)
        ax_bottom.invert_yaxis()
        ax_bottom.set_aspect(1)
        ax_bottom.set_xlabel("[$km$]")
        ax_bottom.set_ylabel("[$km$]")
        def post_processing(bm, ax_right, ax_bottom, wpad=0.05, hpad=0.05):
            (xmin, ymin), (xmax, ymax) = bm.ax.get_position().get_points()
            (xmin0, ymin0), (xmax0, ymax0) = bm.ax.get_position().get_points()
            (xmin_r, ymin_r), (xmax_r, ymax_r) = ax_right.get_position().get_points()
            (xmin_b, ymin_b), (xmax_b, ymax_b) = ax_bottom.get_position().get_points()
            dx0, dy0 = (xmax0-xmin0), (ymax0-ymin0)
            dx_r, dy_r = (xmax_r-xmin_r), (ymax_r-ymin_r)
            dx_b, dy_b = (xmax_b-xmin_b), (ymax_b-ymin_b)
            aspect_r = dy_r / dx_r
            aspect_b = dy_b / dx_b
            ax_right.set_position((xmax0+wpad, ymin0, 0.1, dy0))
            ax_bottom.set_position((xmin0, ymin0-dx0*aspect_b-hpad, dx0, dx0*aspect_b))
        return ((bm, ax_right, ax_bottom), post_processing)

    def plot_slice(self, phase="P", origin=(33.5, -116.5, 0), strike=0,
                   length=50, zmin=0, zmax=25, nx=25, nz=25, ax=None):
        r"""
        Plot an arbitrarily oriented vertical slice from the VelocityModel.
        """
        vv, ned, geo = self.extract_slice(phase=phase,
                                          origin=origin,
                                          strike=strike,
                                          length=length,
                                          zmin=zmin,
                                          zmax=zmax,
                                          nx=nx,
                                          nz=nz)
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, aspect=1)
        xx, yy = ned[..., 0], ned[..., 2]
        qmesh = ax.pcolormesh(xx, yy, vv, cmap=plt.get_cmap("jet_r"))
        ax.invert_yaxis()
        return(ax, qmesh)

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
    #print(v("vp", 33.0, -116.9, 3.0))
    vm = VelocityModel("/Users/malcolcw/Projects/Shared/Velocity/FANG2016/original/Vpvs.dat", "fang")
    with open("/Users/malcolcw/Projects/Wavefront/pywrap/example5/vgrids.in", "w") as outf:
        outf.write(str(vm))
if __name__ == "__main__":
    test()
    print("velocity.py is not an executable script.")
    exit()

