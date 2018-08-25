# coding=utf-8
import numpy as np
import seispy
import fmm3d

class Propagator(seispy.velocity.VelocityModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regularize(self.nodes["nr"],
                        self.nodes["ntheta"],
                        self.nodes["nphi"])
        self.pad(depth=30)
        self.pgrid = self.fit_propagation_grid()
        self.vgrids = np.array(
                [np.stack((np.fliplr(np.copy(self.values["Vp"])),
                           np.fliplr(np.copy(self.values["Vs"]))))]
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
        sources = seispy.geometry.validate_geographic_coords(sources)
        nsources = len(sources)
        receivers = seispy.geometry.validate_geographic_coords(receivers)
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

def write_sources(sources):
    outf = open("/Users/malcolcw/Desktop/rays/sources.rtp", "w")
    for sx in sources:
        r, t, p = seispy.geometry.geo2sph(*sx)
        outf.write("{:.6f} {:.6f} {:.6f}\n".format(r, t, p))
    outf.close()

def write_receivers(receivers):
    outf = open("/Users/malcolcw/Desktop/rays/receivers.rtp", "w")
    for rx in receivers:
        r, t, p = seispy.geometry.geo2sph(*rx)
        outf.write("{:.6f} {:.6f} {:.6f}\n".format(r, t, p))
    outf.close()

def write_rays(rays):
    outfP = open("/Users/malcolcw/Desktop/rays/rays-P.rtp", "w")
    outfS = open("/Users/malcolcw/Desktop/rays/rays-S.rtp", "w")
    outfP.write("{:d}\n".format(rays.shape[0]*rays.shape[1]))
    outfS.write("{:d}\n".format(rays.shape[0]*rays.shape[1]))
    for sx in rays:
        for rayP, rayS in sx:
            outfP.write("{:d}\n".format(len([px for px in rayP if not np.any(px.mask)])))
            outfS.write("{:d}\n".format(len([px for px in rayS if not np.any(px.mask)])))
            rayP[:,1] *= -1
            rayP[:,1] += np.pi / 2
            rayS[:,1] *= -1
            rayS[:,1] += np.pi / 2
            for px in np.array([px for px in rayP if not np.any(px.mask)]):
                outfP.write("{:.6f} {:.6f} {:.6f}\n".format(*px))
            for px in np.array([px for px in rayS if not np.any(px.mask)]):
                outfS.write("{:.6f} {:.6f} {:.6f}\n".format(*px))
    outfP.close()
    outfS.close()

if __name__ == "__main__":
    prop = Propagator("/Users/malcolcw/Projects/Shared/Velocity/FANG2016/original/VpVs.dat", "fang", topo=seispy.topography.Topography("/Users/malcolcw/Projects/Shared/Topography/anza.xyz"))
    #prop = Propagator("/Users/malcolcw/Desktop/IASP91.fang.txt", "fang", topo=seispy.topography.Topography("/Users/malcolcw/Projects/Shared/Topography/anza.xyz"))
    latmin = np.degrees(np.pi / 2 - prop.nodes["theta"][0,-2,0])
    latmax = np.degrees(np.pi / 2 - prop.nodes["theta"][0,1,0])
    lonmin = np.degrees(prop.nodes["phi"][0,0,1])
    lonmax = np.degrees(prop.nodes["phi"][0,0,-2])
    dlat = (latmax - latmin)
    dlon = (lonmax - lonmin)
    lat0 = np.mean([latmin, latmax])
    lon0 = np.mean([lonmin, lonmax])

    sources = np.array([[lat0 - 0.25*dlat, lon0 - 0.25*dlon, 15]])
    receivers = np.empty((4,3))
    receivers[:,:2] = [[lat0 - 0.25*dlat, lon0 - 0.25*dlon],
                       [lat0 + 0.25*dlat, lon0 - 0.25*dlon],
                       [lat0 + 0.25*dlat, lon0 + 0.25*dlon],
                       [lat0 - 0.25*dlat, lon0 + 0.25*dlon]]

    receivers[:,2] = np.array([prop.topo(*receivers[i,:2]) - seispy.constants.EARTH_RADIUS
                                for i in range(len(receivers))])
    rays, tts = prop(sources, receivers)
    #plot(rays)
    write_rays(rays)
    write_sources(sources)
    write_receivers(receivers)
