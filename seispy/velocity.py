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
            self.topo = lambda: seispy.constants.EARTH_RADIUS
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
            raise(ValueError("point above surface"))
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

    def print_fm3d(self, phase, propgrid, stretch=1.01, size_ratio=2, basement=30):
        phase = _verify_phase(phase)
        return(self.print_propgrid(propgrid),
               self.print_vgrid(phase,
                                propgrid,
                                stretch=stretch,
                                size_ratio=2),
               self.print_interfaces(propgrid,
                                     stretch=stretch,
                                     size_ratio=size_ratio,
                                     basement=basement))

    def print_interfaces(self, propgrid, stretch=1.01, size_ratio=2, basement=30):
        igrid = _calculate_grid_parameters(propgrid)
        nlat, nlon = igrid["nlat"], igrid["nlon"]
        dlat, dlon = radians(igrid["dlat"]), radians(igrid["dlon"])
        lat0, lon0 = radians(igrid["lat0"]), radians(igrid["lon0"])
        blob = "2\n"\
               "{:d} {:d}\n"\
               "{:.4f} {:.4f}\n"\
               "{:.4f} {:.4f}\n".format(nlat, nlon,
                                        dlat, dlon,
                                        lat0, lon0)
        for r in (seispy.constants.EARTH_RADIUS + 5,
                  seispy.constants.EARTH_RADIUS - basement):
            for ilat, ilon in [(ilat, ilon) for ilat in range(nlat)
                                            for ilon in range(nlon)]:
                blob += "{:.4f}\n".format(r)
        return(blob.rstrip())

    def print_propgrid(self, grid):
        return("{:d} {:d} {:d}\n"\
               "{:.6f} {:.6f} {:.6f}\n"\
               "{:.6f} {:.6f} {:.6f}\n"\
               "5 10".format(grid["nr"], grid["nlat"], grid["nlon"],
                             grid["dr"], grid["dlat"], grid["dlon"],
                             grid["h0"], grid["lat0"], grid["lon0"]))

    def print_vgrid(self, phase, propgrid, stretch=1.01, size_ratio=2):
        phase = _verify_phase(phase)
        vgrid = _calculate_grid_parameters(propgrid)
        nr, nlat, nlon = vgrid["nr"], vgrid["nlat"], vgrid["nlon"]
        dr, dlat, dlon = vgrid["dr"], radians(vgrid["dlat"]), radians(vgrid["dlon"])
        r0, lat0, lon0 = vgrid["r0"], radians(vgrid["lat0"]), radians(vgrid["lon0"])
        blob = "{:d} {:d} {:d}\n"\
               "{:.4f} {:.4f} {:.4f}\n"\
               "{:.4f} {:.4f} {:.4f}\n".format(nr, nlat, nlon,
                                               dr, dlat, dlon,
                                               r0, lat0, lon0)
        for (ir, ilat, ilon) in [(ir, ilat, ilon) for ir in range(nr)\
                                                  for ilat in range(nlat)\
                                                  for ilon in range(nlon)]:
            lat = degrees(lat0 + dlat * ilat)
            lon = degrees(lon0 + dlon * ilon) % 360.
            r = r0 + dr * ir
            depth = seispy.constants.EARTH_RADIUS - r
            blob += "{:f}\n".format(self(phase, lat, lon, depth))
        return(blob.rstrip())

def _calculate_grid_parameters(grid, stretch=1.01, size_ratio=2):
        pnr, pnlat, pnlon = grid["nr"], grid["nlat"], grid["nlon"]
        pdr, pdlat, pdlon = grid["dr"], radians(grid["dlat"]), radians(grid["dlon"])
        ph0, plat0, plon0 = grid["h0"], radians(grid["lat0"]), radians(grid["lon0"])
        pr0, ptheta0, pphi0 = seispy.geometry.geo2sph(grid["lat0"],
                                                      grid["lon0"],
                                                      -grid["h0"])
        plat0, plon0 = ptheta0, pphi0
        pr0 = seispy.constants.EARTH_RADIUS + ph0 - ((pnr - 1) * pdr)
        i = (pnr - 1) % size_ratio
        pnr = pnr + (size_ratio - i) if i > 0 else pnr
        i = (pnlat - 1) % size_ratio
        pnlat = pnlat + (size_ratio - i) if i > 0 else pnlat
        i = (pnlon - 1) % size_ratio
        pnlon = pnlon + (size_ratio - i) if i > 0 else pnlon
        nr = int((pnr - 1) / size_ratio) + 3
        nlat = int((pnlat - 1) / size_ratio) + 3
        nlon = int((pnlon - 1) / size_ratio) + 3
        dr = stretch * pdr * size_ratio
        dlat = stretch * pdlat * size_ratio
        dlon = stretch * pdlon * size_ratio
        r0 = pr0 - dr - (nr - 1) * dr * (stretch - 1) / 2
        lat0 = plat0 - dlat - (nlat - 1) * dlat * (stretch - 1) / 2
        lon0 = plon0 - dlon - (nlon - 1) * dlon * (stretch - 1) / 2
        return({"nr": nr, "nlat": nlat, "nlon": nlon,
                "dr": dr, "dlat": dlat, "dlon": dlon,
                "r0": r0, "lat0": lat0, "lon0": lon0})

def _verify_phase(phase):
    if phase.upper() == "P" or  phase.upper() == "VP":
        phase = "Vp"
    elif phase.upper() == "S" or phase.upper() == "VS":
        phase = "Vs"
    else:
        raise(ValueError("invalid phase type - {}".format(phase)))
    return(phase)
