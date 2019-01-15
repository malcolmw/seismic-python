# coding=utf-8
import numpy as np
import pandas as pd

from collections import deque
from . import constants as _constants
from . import coords as _coords
from . import geogrid as _geogrid
from . import velocity as _velocity

ER = _constants.EARTH_RADIUS
pi = np.pi

def print_fm3d(vm):
    if not vm._is_regular:
        raise(NotImplementedError('only regular velocity grids can be '
                                    'written to FM3D format'))
    s = '1\t2\n'
    s += f'{vm._nR}\t{vm._nT}\t{vm._nP}\n'
    s += f'{vm._dr}\t{vm._dt}\t{vm._dp}\n'
    s += f'{vm._R0}\t{vm._L0}\t{vm._P0}\n'
    s += '\n'.join(vm._vp.flatten().astype(str))
    s += '\n'
    s += f'{vm._nR}\t{vm._nT}\t{vm._nP}\n'
    s += f'{vm._dr}\t{vm._dt}\t{vm._dp}\n'
    s += f'{vm._R0}\t{vm._L0}\t{vm._P0}\n'
    s += '\n'.join(vm._vs.flatten().astype(str))
    s += '\n'
    return (s)

def print_fm3d_interfaces(vm,
                          i1=_constants.EARTH_RADIUS,
                          i2=_constants.EARTH_RADIUS-30):
    if not vm._is_regular:
        raise(NotImplementedError('only regular velocity grids can be '
                                    'written to FM3D format'))
    s = '2\n'
    s += f'{vm._nT}\t{vm._nP}\n'
    s += f'{vm._dt}\t{vm._dt}\n'
    s += f'{vm._L0}\t{vm._P0}\n'
    n = vm._nT * vm._nP
    s += '\n'.join((str(i1) for i in range(n)))
    s += '\n'
    s += '\n'.join(str(i2) for i in range(n))
    s += '\n'
    return(s)

def print_fm3d_propgrid(vm,
                        dr=None,
                        dt=None,
                        dp=None,
                        refinement_factor=5,
                        n_refined_propgrid_cells=10):
    dr = vm._dr if dr is None else dr
    dt = vm._dt if dt is None else dt
    dp = vm._dp if dp is None else dp
    (rmin, rmax), (tmin, tmax), (pmin, pmax) = vm.get_bounds()
    nnr = int((rmax - rmin - 2 * vm._dr) / dr)
    nnt = int((tmax - tmin - 2 * vm._dt) / dt)
    nnp = int((pmax - pmin - 2 * vm._dp) / dp)
    r0, t0, p0 = vm.get_center()
    if nnr % 2 == 0:
        r_min = r0 - dr * ((nnr - 1)/2)
        r_max = r0 + dr * ((nnr - 1)/2)
    else:
        r_min = r0 - dr * int(nnr / 2)
        r_max = r0 + dr * (nnr - 1 - int(nnr / 2))
    if nnt % 2 == 0:
        t_min = t0 - dt * ((nnt - 1)/2)
        t_max = t0 + dt * ((nnt - 1)/2)
    else:
        t_min = t0 - dt * int(nnt / 2)
        t_max = t0 + dt * (nnt - 1 - int(nnt / 2))
    if nnp % 2 == 0:
        p_min = p0 - dp * ((nnp - 1)/2)
        p_max = p0 + dp * ((nnp - 1)/2)
    else:
        p_min = p0 - dp * int(nnp / 2)
        p_max = p0 + dp * (nnp - 1 - int(nnp / 2))
# # of propagation grid points in r, lat and long
    s = f'{nnr}\t{nnt}\t{nnp}\n'
# grid intervals in r (km) lat,long (deg
    s += f'{dr}\t{np.degrees(dt)}\t{np.degrees(dp)}\n'
# origin of the grid height (km),lat,long (deg)
    s += f'{r_max-_constants.EARTH_RADIUS}\t'
    s += f'{np.degrees(np.pi/2-t_max)}\t'
    s += f'{np.degrees(p_min)}\t\n'
# refinement factor and # of propgrid cells in refined source grid
    s += f'{refinement_factor}\t{n_refined_propgrid_cells}\n'
    return(s)

def format_interfaces(interfaces):
    grid = interfaces[0].grid
    blob = "{:d}\n".format(len(interfaces))
    blob += "{:d} {:d}\n".format(grid.nlambda, grid.nphi)
    blob += "{:.15f} {:.15f}\n".format(np.float64(grid.dlambda), np.float64(grid.dphi))
    blob += "{:.15f} {:.15f}\n".format(grid.lambda0, grid.phi0)
    for interface in interfaces:
        coordinates = np.flipud(interface.coordinates)
        for (ilambda, iphi) in [(ilambda, iphi) for ilambda in range(grid.nlambda)
                                  for iphi in range(grid.nphi)]:
            blob += "{:.15f}\n".format(coordinates[ilambda, iphi, 0])
    return(blob)

def format_propagation_grid(grid):
    blob = "{:3d} {:3d} {:3d}\n".format(grid.nrho, grid.nlat, grid.nlon)
    blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.drho, grid.dlat, grid.dlon)
    blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(-grid.depth0, grid.lat0, grid.lon0)
    blob += "5 10\n"
    return(blob)

def format_receivers(receivers):
    blob = "{:d}\n".format(len(receivers))
    blob += "".join([str(r) for r in receivers])
    return(blob)

def format_sources(sources):
    blob = "{:d}\n".format(len(sources))
    blob += "".join([str(s) for s in sources])
    return(blob)

def format_vgrids(vmodel):
    blob = "{:d} {:d}\n".format(vmodel.nvgrids, vmodel.nvtypes)
    for (typeID, gridID) in [(typeID, gridID)
                             for typeID in range(1, vmodel.nvtypes + 1)
                             for gridID in range(1, vmodel.nvgrids+ 1 )]:
        grid = vmodel.v_type_grids[typeID][gridID]["grid"]
        blob += "{:d} {:d} {:d}\n".format(grid.nrho,
                                          grid.nlambda,
                                          grid.nphi)
        blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.drho,
                                                      grid.dlambda,
                                                      grid.dphi)
        blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.rho0,
                                                      grid.lambda0,
                                                      grid.phi0)
        for irho, ilambda, iphi in ((i, j, k) for i in range(grid.nrho)
                                for j in range(grid.nlambda)
                                for k in range(grid.nphi)):
            lat, lon, depth = _coords.as_left_spherical([grid.rho0 + irho * grid.drho,
                                                        grid.lambda0 + ilambda * grid.dlambda,
                                                        grid.phi0 + iphi * grid.dphi]).to_geographic()
            blob += "{:11.6f}\n".format(vmodel(typeID, gridID, lat, lon, depth ))
    return(blob)

def read_arrtimes(inf):
    with open(inf, 'r') as inf:
        data = deque(inf.read().split('\n'))
    nr, nlat, nlon = (int(v) for v in data.popleft().split())
    dr, dlat, dlon = (float(v) for v in data.popleft().split())
    r0, lat0, lon0 = (float(v) for v in data.popleft().split())
    nset = int(data.popleft())
    isrc, ipath, _ = (int(v) for v in data.popleft().split())
    nn = nr * nlat * nlon
    tt = np.array([float(data.popleft()) for i in range(nn)])
    r_nodes = np.array([r0 + i * dr for i in range(nr)])
    lat_nodes = np.array([(lat0 + i * dlat)
                        for i in range(nlat)])
    lon_nodes = np.array([lon0 + i * dlon for i in range(nlon)])
    lon_mesh, lat_mesh, r_mesh = np.meshgrid(lon_nodes,
                                            lat_nodes,
                                            r_nodes,
                                            indexing='ij')
    geo = _coords.as_geographic(np.stack([lat_mesh.flatten(),
                                          lon_mesh.flatten(),
                                          -r_mesh.flatten() + ER],
                                          axis=1))
    df = pd.DataFrame({'lat': geo[:, 0],
                        'lon': geo[:, 1],
                        'depth': geo[:, 2],
                        'value': tt})
    return (df)


def read_interfaces(infile):
    infile = open(infile)
    ninter = int(infile.readline().split()[0])
    nlambda, nphi = [int(v) for v in infile.readline().split()[:2]]
    dlambda, dphi = [np.float64(v) for v in infile.readline().split()[:2]]
    lambda0, phi0 = [np.float64(v) for v in infile.readline().split()[:2]]
    grid = _geogrid.GeoGrid2D(np.degrees(lambda0), np.degrees(phi0),
                             nlambda, nphi,
                             np.degrees(dlambda), np.degrees(dphi))
    interfaces = []
    for iinter in range(ninter):
        surf = _surface.GeoSurface()
        surf.grid = grid
        coordinates = _coords.as_left_spherical([[[np.float64(infile.readline().split()[0]),
                                                  lambda0 + ilambda*dlambda,
                                                  phi0 + iphi*dphi]
                                                for iphi in range(nphi)]
                                                for ilambda in range(nlambda)])
        coordinates = np.flip(coordinates.to_spherical(), axis=0)
        surf.coordinates = coordinates
        interfaces.append(surf)
    return(interfaces)

def read_propgrid(inf):
    with open(inf, 'r') as inf:
        data = deque(inf.read().split('\n'))
    ndepth, nlat, nlon = (int(v) for v in data.popleft().split())
    ddepth, dlat, dlon = (float(v) for v in data.popleft().split())
    h0, lat0, lon0 = (float(v) for v in data.popleft().split())
    depth_nodes = [-h0 + i * ddepth for i in range(ndepth)]
    lat_nodes = [lat0 + i * dlat for i in range(nlat)]
    lon_nodes = [lon0 + i* dlon for i in range(nlon)]
    lat_mesh, lon_mesh, depth_mesh = np.meshgrid(lat_nodes,
                                                  lon_nodes,
                                                  depth_nodes,
                                                 indexing='ij')
    pgrid = _coords.as_geographic(np.stack((lat_mesh.flatten(),
                                            lon_mesh.flatten(),
                                            depth_mesh.flatten()),
                                           axis=1)).reshape(nlat, nlon, ndepth, 3)
    pgrid.dlat = np.unique(np.diff(np.unique(pgrid[..., 0])))[0]
    pgrid.dlon = np.unique(np.diff(np.unique(pgrid[..., 1])))[0]
    pgrid.ddepth = np.unique(np.diff(np.unique(pgrid[..., 2])))[0]
    pgrid.dr = pgrid.ddepth
    pgrid.dt = np.radians(pgrid.dlat)
    pgrid.dp = np.radians(pgrid.dlon)
    return (pgrid)

def read_source(inf):
    with open(inf, 'r') as inf:
        data = deque(inf.read().split('\n'))
    data.popleft()
    data.popleft()
    depth, lat, lon = (float(v) for v in data.popleft().split()[:3])
    return (_coords.as_geographic((lat, lon, depth)))

def read_receivers(infile):
    infile = open(infile)
    nrec = int(infile.readline().split()[0])
    receivers = []
    for irec in range(nrec):
        depth, lat, lon = [np.float64(v) for v in infile.readline().split()[:3]]
        lat, lon, depth = _coords.as_geographic([lat, lon, depth])
        receivers.append(Receiver(lat, lon, depth))
        npath = int(infile.readline().split()[0])
        path_sourceID = [int(v) for v in infile.readline().split()[:npath]]
        pathID = [int(v) for v in infile.readline().split()[:npath]]
        for ipath in range(npath):
            receivers[irec].add_path(RayPath(path_sourceID[ipath], pathID[ipath]))
    return(receivers)

#def read_sources(infile):
#    infile = open(infile)
#    nsrc = int(infile.readline().split()[0])
#    sources = []
#    for sourceID in range(1, nsrc+1):
#        is_tele = True if int(infile.readline().split()[0]) == 1 else False
#        if is_tele:
#            phase = infile.readline().split()[0]
#        depth, lat, lon = [np.float64(v) for v in infile.readline().split()[:3]]
#        lat, lon, depth = _coords.as_geographic([lat, lon, depth])
#        if is_tele:
#            sources.append(Source(sourceID, lat, lon, depth, is_tele, phase))
#        else:
#            sources.append(Source(sourceID, lat, lon, depth, is_tele))
#        npath = int(infile.readline().split()[0])
#        for pathID in range(1, npath+1):
#            nsection = int(infile.readline().split()[0])
#            sections = [int(v) for v in infile.readline().split()[:2*nsection]]
#            vtypes = [int(v) for v in infile.readline().split()[:nsection]]
#            path = RayPath(sourceID, pathID)
#            for isec in range(nsection):
#                path.add_section(RayPathSection(*sections[isec*2:isec*2+2],
#                                                vtypes[isec]))
#            sources[-1].add_path(path)
#    return(sources)

class RayPath(object):
    def __init__(self, sourceID, pathID):
        self.sourceID = sourceID
        self.pathID = pathID
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

class RayPathSection(object):
    def __init__(self, start, stop, vtype):
        self.start = start
        self.stop = stop
        self.vtype = vtype

class Receiver(object):
    def __init__(self, lat, lon, depth):
        self.lat, self.lon, self.depth = lat, lon, depth
        self.paths = []

    def add_path(self, path):
        self.paths.append(path)

    def __str__(self):
        blob = "{:.15f} {:.15f} {:.15f}\n".format(self.depth, self.lat, self.lon)
        blob += "{:d}\n".format(len(self.paths))
        for path in self.paths:
            blob += "{:d} ".format(path.sourceID)
        blob += "\n"
        for path in self.paths:
            blob += "{:d} ".format(path.pathID)
        blob += "\n"
        return(blob)

class Source(object):
    def __init__(self, sourceID, lat, lon, depth, is_tele, phase=None):
        self.sourceID = 1
        self.lat, self.lon, self.depth = lat, lon, depth
        self.is_tele = is_tele
        self.phase = phase
        self.paths = []

    def add_path(self, path):
        self.paths.append(path)

    def __str__(self):
        blob = "1\n" if self.is_tele else "0\n"
        if self.is_tele:
            blob += "{:s}\n".format(self.phase)
        blob += "{:.15f} {:.15f} {:.15f}\n".format(self.depth, self.lat, self.lon)
        blob += "{:d}\n".format(len(self.paths))
        for path in self.paths:
            blob += "{:d}\n".format(len(path.sections))
            for section in path.sections:
                blob += "{:d} {:d}  ".format(section.start, section.stop)
            blob += "\n"
            for section in path.sections:
                blob += "{:d}    ".format(section.vtype)
            blob += "\n"
        return(blob)

def test_io():
    rootin = "/Users/malcolcw/Projects/Wavefront/examples/example3"
    rootout = "/Users/malcolcw/Projects/Wavefront/stock-replicate/example3"
    receivers = read_receivers("%s/receivers.in" % rootin)
    sources = read_sources("%s/sources.in" % rootin)
    interfaces = read_interfaces("%s/interfaces.in" % rootin)
    vmodel = _velocity.VelocityModel("%s/vgrids.in" % rootin, "fmm3d")
    with open("%s/vgrids.in" % rootout, "w") as f:
        f.write(format_vgrids(vmodel))
    with open("%s/interfaces.in" % rootout, "w") as f:
        f.write(format_interfaces(interfaces))
    with open("%s/receivers.in" % rootout, "w") as f:
        f.write(format_receivers(receivers))
    with open("%s/sources.in" % rootout, "w") as f:
        f.write(format_sources(sources))

if __name__ == "__main__":
    test_io()

