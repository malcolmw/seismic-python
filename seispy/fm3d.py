def print_fm3d(vm, phase, propgrid, stretch=1.01, size_ratio=2, basement=30):
    return(vm.print_propgrid(propgrid),
           vm.print_vgrid(phase,
                          propgrid,
                          stretch=stretch,
                          size_ratio=2),
           vm.print_interfaces(propgrid,
                               stretch=stretch,
                               size_ratio=size_ratio,
                               basement=basement))

def print_interfaces(vm, propgrid, stretch=1.01, size_ratio=2, basement=30):
    igrid = _calculate_grid_parameters(propgrid)
    ntheta, nphi = igrid["ntheta"], igrid["nphi"]
    dtheta, dphi = radians(igrid["dtheta"]), radians(igrid["dphi"])
    theta0, phi0 = radians(igrid["theta0"]), radians(igrid["phi0"])
    blob = "2\n"\
           "{:d} {:d}\n"\
           "{:.4f} {:.4f}\n"\
           "{:.4f} {:.4f}\n".format(ntheta, nphi,
                                    dtheta, dphi,
                                    theta0, phi0)
    for r in (seispy.constants.EARTH_RADIUS + 5,
              seispy.constants.EARTH_RADIUS - basement):
        for itheta, iphi in [(itheta, iphi) for itheta in range(ntheta)
                                            for iphi in range(nphi)]:
            blob += "{:.4f}\n".format(r)
    return(blob.rstrip())

def print_propgrid(vm, grid):
    return("{:d} {:d} {:d}\n"\
           "{:.6f} {:.6f} {:.6f}\n"\
           "{:.6f} {:.6f} {:.6f}\n"\
           "5 10".format(grid["nr"], grid["nlat"], grid["nlon"],
                         grid["dr"], grid["dlat"], grid["dlon"],
                         grid["h0"], grid["lat0"], grid["lon0"] % 360))

def print_vgrid(vm, phase, propgrid, stretch=1.01, size_ratio=2):
    vgrid = _calculate_grid_parameters(propgrid)
    nr, ntheta, nphi = vgrid["nr"], vgrid["ntheta"], vgrid["nphi"]
    dr, dtheta, dphi = vgrid["dr"], radians(vgrid["dtheta"]), radians(vgrid["dphi"])
    r0, theta0, phi0 = vgrid["r0"], radians(vgrid["theta0"]), radians(vgrid["phi0"])
    blob = "{:d} {:d} {:d}\n"\
            "{:.4f} {:.4f} {:.4f}\n"\
            "{:.4f} {:.4f} {:.4f}\n".format(nr, ntheta, nphi,
                                            dr, dtheta, dphi,
                                            r0, theta0, phi0)
    for (ir, itheta, iphi) in [(ir, itheta, iphi) for ir in range(nr)\
                                                  for itheta in range(ntheta)\
                                                  for iphi in range(nphi)]:
        lat = degrees(theta0 + dtheta * itheta)
        lon = degrees(phi0 + dphi * iphi) % 360.
        r = r0 + dr * ir
        depth = seispy.constants.EARTH_RADIUS - r
        blob += "{:f}\n".format(vm(phase, lat, lon, depth))
    return(blob.rstrip())

def _calculate_grid_parameters(grid, stretch=1.01, size_ratio=2):
    pnr, pntheta, pnphi = grid["nr"], grid["nlat"], grid["nlon"]
    pdr, pdtheta, pdphi = grid["dr"], radians(grid["dlat"]), radians(grid["dlon"])
    pr0, ptheta0, pphi0 = seispy.geometry.geo2sph(grid["lat0"],
                                                    grid["lon0"],
                                                    -grid["h0"])
#    plat0, plon0 = ptheta0, pphi0
#    pr0 = seispy.constants.EARTH_RADIUS + ph0 - ((pnr - 1) * pdr)
    i = (pnr - 1) % size_ratio
    pnr = pnr + (size_ratio - i) if i > 0 else pnr
    i = (pntheta - 1) % size_ratio
    pntheta = pntheta + (size_ratio - i) if i > 0 else pntheta
    i = (pnphi - 1) % size_ratio
    pnphi = pnphi + (size_ratio - i) if i > 0 else pnphi
    nr = int((pnr - 1) / size_ratio) + 3
    ntheta = int((pntheta - 1) / size_ratio) + 3
    nphi = int((pnphi - 1) / size_ratio) + 3
    dr = stretch * pdr * size_ratio
    dtheta = stretch * pdtheta * size_ratio
    dphi = stretch * pdphi * size_ratio
    r0 = pr0 - dr - (nr - 1) * dr * (stretch - 1) / 2
    theta0 = ptheta0 - dtheta - (ntheta - 1) * dtheta * (stretch - 1) / 2
    phi0 = pphi0 - dphi - (nphi - 1) * dphi * (stretch - 1) / 2
    return({"nr": nr, "ntheta": ntheta, "nphi": nphi,
            "dr": dr, "dtheta": dtheta, "dphi": dphi,
            "r0": r0, "theta0": theta0, "phi0": phi0})
