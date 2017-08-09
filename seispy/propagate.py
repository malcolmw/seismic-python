import numpy as np
import seispy
import velocity
import fm3d

class Propagator(velocity.VelocityModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.regularize(2 * self.nodes["nr"],
        self.regularize(self.nodes["nr"],
                        self.nodes["ntheta"],
                        self.nodes["nphi"])
        self.pad(depth=30)
        self.pgrid = self.fit_propagation_grid()
        self.vgrids = np.array(
                [np.stack((np.fliplr(np.flipud(np.copy(self.values["Vp"]))),
                 np.fliplr(np.flipud(np.copy(self.values["Vs"])))))]
                              )
        fm3d.initialize_propagation_grid(**self.pgrid)
        fm3d.initialize_velocity_grids(self.vgrids,
                                       *self.vgrids.shape,
                                       self.nodes["r_min"],
                                       np.pi/2 - self.nodes["theta_max"],
                                       self.nodes["phi_min"],
                                       self.nodes["dr"],
                                       self.nodes["dtheta"],
                                       self.nodes["dphi"])
        fm3d.initialize_interfaces(np.pi/2 - self.nodes["theta_max"],
                                   self.nodes["phi_min"],
                                   self.nodes["ntheta"],
                                   self.nodes["nphi"],
                                   self.nodes["dtheta"],
                                   self.nodes["dphi"])

    def __call__(self, sources, receivers):
        sources[:,1] %= 360.
        nsources = len(sources)
        receivers[:,1] %= 360.
        nreceivers = len(receivers)
        rays = np.zeros((nsources, nreceivers, 2, 10000, 3),
                            order="F",
                            dtype=np.float32) - 999.
        tts = np.empty((nsources, nreceivers, 2),
                        order="F",
                        dtype=np.float32)
        fm3d.run(sources, nsources, receivers, nreceivers, rays, tts)
        rays = np.ma.masked_equal(rays, -999.)
        return(rays, tts)

    def fit_propagation_grid(self,
                             nr=None,
                             nlat=None,
                             nlon=None):
        nr = self.nodes["nr"] if nr is None else nr
        nlat = self.nodes["ntheta"] if nlat is None else nlat
        nlon = self.nodes["nphi"] if nlon is None else nlon

        rmin = self.nodes["r"][0,0,0] + self.nodes["dr"] * 1.01
        rmax = self.nodes["r"][-1,0,0] - self.nodes["dr"] * 1.01
        dr = (rmax - rmin) / (nr - 1)

        latmin = np.degrees(np.pi / 2\
                          - self.nodes["theta"][0,-2,0]\
                          + (self.nodes["dtheta"] * 0.01))
        latmax = np.degrees(np.pi / 2\
                          - self.nodes["theta"][0,1,0]\
                          - (self.nodes["dtheta"] * 0.01))
        dlat = (latmax - latmin) / (nlat - 1)

        lonmin = np.degrees(self.nodes["phi"][0,0,1]\
                          + self.nodes["dphi"] * 0.01)
        lonmax = np.degrees(self.nodes["phi"][0,0,-2]\
                          - self.nodes["dphi"] * 0.01)
        dlon = (lonmax - lonmin) / (nlon - 1)
        return({"h0": rmax - seispy.constants.EARTH_RADIUS, "dr": dr, "nr": nr,
                "lat0": latmin, "dlat": dlat, "nlat": nlat,
                "lon0": lonmin, "dlon": dlon, "nlon": nlon})

    def pad(self, depth=None):
        nodes = self.nodes

        dr = (nodes["r"][-1,0,0] - nodes["r"][0,0,0]) / (nodes["nr"] - 1)
        rmin = nodes["r"][0,0,0] - dr if depth is None\
                else seispy.constants.EARTH_RADIUS - depth
        rmax = np.max(self.topo.radius) + 2 * dr
        r_nodes = np.linspace(rmin, rmax, round((rmax - rmin) / dr))

        dtheta = nodes["theta"][0,1,0] - nodes["theta"][0,0,0]
        t_nodes = np.insert(nodes["theta"][0,:,0],
                            0,
                            nodes["theta_min"] - dtheta)
        dtheta = nodes["theta"][0,-1,0] - nodes["theta"][0,-2,0]
        t_nodes = np.insert(t_nodes,
                            len(t_nodes),
                            nodes["theta_max"] + dtheta)

        dphi = nodes["phi"][0,0,1] - nodes["phi"][0,0,0]
        p_nodes = np.insert(nodes["phi"][0,0,:],
                            0,
                            nodes["phi_min"] - dphi)
        dphi = nodes["phi"][0,0,-1] - nodes["phi"][0,0,-2]
        p_nodes = np.insert(p_nodes,
                            len(p_nodes),
                            nodes["phi_max"] + dphi)
        R, T, P = np.meshgrid(r_nodes, t_nodes, p_nodes, indexing="ij")
        self.regrid(R, T, P)

if __name__ == "__main__":
    prop = Propagator("/Users/malcolcw/Projects/Shared/Velocity/FANG2016/original/VpVs.dat", "fang", topo=seispy.topography.Topography("/Users/malcolcw/Projects/Shared/Topography/anza.xyz"))
    #sources = np.array([[33., 242., 5.0],
    #                    [33., 242.5, 10.],
    #                    [33., 243., 15.],
    #                    [33., 243.5, 19.]])
    #receivers = np.array([[33., 242., 0.0],
    #                      [33., 242.5, 0.0],
    #                      [33., 243, 0.0],
    #                      [33., 243.5, 0.0]])
    sources = np.array([[33., 242., 5.0]])
    receivers = np.array([[33., 242.9, 0.0]])
    rays, tts = prop(sources, receivers)

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    rays[:,:,1,:,1] *= -1
    rays[:,:,1,:,1] += np.pi / 2
    ray = np.array([seispy.geometry.sph2xyz(*r) for r in rays[0,0,1] if not np.any(r.mask)])
    ax.plot(ray[:,0], ray[:,1], ray[:,2])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()

