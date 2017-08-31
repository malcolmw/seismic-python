import numpy as np
import seispy
ER = seispy.constants.EARTH_RADIUS

π = np.pi

def format_interfaces(interfaces):
    grid = interfaces[0].grid
    blob = "{:d}\n".format(len(interfaces))
    blob += "{:d} {:d}\n".format(grid.nλ, grid.nφ)
    blob += "{:.15f} {:.15f}\n".format(np.float64(grid.dλ), np.float64(grid.dφ))
    blob += "{:.15f} {:.15f}\n".format(grid.λ0, grid.φ0)
    for interface in interfaces:
        coordinates = np.flipud(interface.coordinates)
        for (iλ, iφ) in [(iλ, iφ) for iλ in range(grid.nλ)
                                  for iφ in range(grid.nφ)]:
            blob += "{:.15f}\n".format(coordinates[iλ, iφ, 0])
    return(blob)

def format_propagation_grid(grid):
    blob = "{:3d} {:3d} {:3d}\n".format(grid.nr, grid.nlat, grid.nlon)
    blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.dr, grid.dlat, grid.dlon)
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
        blob += "{:d} {:d} {:d}\n".format(grid.nρ,
                                          grid.nλ,
                                          grid.nφ)
        blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.dρ,
                                                      grid.dλ,
                                                      grid.dφ)
        blob += "{:11.6f} {:11.6f} {:11.6f}\n".format(grid.ρ0,
                                                      grid.λ0,
                                                      grid.φ0)
        for iρ, iλ, iφ in ((i, j, k) for i in range(grid.nρ)
                                for j in range(grid.nλ)
                                for k in range(grid.nφ)):
            lat, lon, depth = seispy.coords.as_left_spherical([grid.ρ0 + iρ * grid.dρ,
                                                        grid.λ0 + iλ * grid.dλ,
                                                        grid.φ0 + iφ * grid.dφ]).to_geographic()
            blob += "{:11.6f}\n".format(vmodel(typeID, gridID, lat, lon, depth ))
    return(blob)

def read_interfaces(infile):
    infile = open(infile)
    ninter = int(infile.readline().split()[0])
    nλ, nφ = [int(v) for v in infile.readline().split()[:2]]
    dλ, dφ = [np.float64(v) for v in infile.readline().split()[:2]]
    λ0, φ0 = [np.float64(v) for v in infile.readline().split()[:2]]
    grid = seispy.geogrid.GeoGrid2D(np.degrees(λ0), np.degrees(φ0),
                             nλ, nφ,
                             np.degrees(dλ), np.degrees(dφ))
    interfaces = []
    for iinter in range(ninter):
        surf = seispy.surface.GeoSurface()
        surf.grid = grid
        coordinates = seispy.coords.as_left_spherical([[[np.float64(infile.readline().split()[0]),
                                                  λ0 + iλ*dλ,
                                                  φ0 + iφ*dφ]
                                                for iφ in range(nφ)]
                                                for iλ in range(nλ)])
        coordinates = np.flip(coordinates.to_spherical(), axis=0)
        surf.coordinates = coordinates
        interfaces.append(surf)
    return(interfaces)

def read_propgrid(infile):
    infile = open(infile, "r")
    nr, nlat, nlon = [int(v) for v in infile.readline().split()[:3]]
    dr, dlat, dlon = [float(v) for v in infile.readline().split()[:3]]
    h0, lat0, lon0 = [float(v) for v in infile.readline().split()[:3]]
    return(seispy.geogrid.GeoGrid3D(lat0, lon0, -h0,
                                    nlat, nlon, nr,
                                    dlat, dlon, dr))

def read_receivers(infile):
    infile = open(infile)
    nrec = int(infile.readline().split()[0])
    receivers = []
    for irec in range(nrec):
        depth, lat, lon = [np.float64(v) for v in infile.readline().split()[:3]]
        lat, lon, depth = seispy.coords.as_geographic([lat, lon, depth])
        receivers.append(Receiver(lat, lon, depth))
        npath = int(infile.readline().split()[0])
        path_sourceID = [int(v) for v in infile.readline().split()[:npath]]
        pathID = [int(v) for v in infile.readline().split()[:npath]]
        for ipath in range(npath):
            receivers[irec].add_path(RayPath(path_sourceID[ipath], pathID[ipath]))
    return(receivers)

def read_sources(infile):
    infile = open(infile)
    nsrc = int(infile.readline().split()[0])
    sources = []
    for sourceID in range(1, nsrc+1):
        is_tele = True if int(infile.readline().split()[0]) == 1 else False
        if is_tele:
            phase = infile.readline().split()[0]
        depth, lat, lon = [np.float64(v) for v in infile.readline().split()[:3]]
        lat, lon, depth = seispy.coords.as_geographic([lat, lon, depth])
        if is_tele:
            sources.append(Source(sourceID, lat, lon, depth, is_tele, phase))
        else:
            sources.append(Source(sourceID, lat, lon, depth, is_tele))
        npath = int(infile.readline().split()[0])
        for pathID in range(1, npath+1):
            nsection = int(infile.readline().split()[0])
            sections = [int(v) for v in infile.readline().split()[:2*nsection]]
            vtypes = [int(v) for v in infile.readline().split()[:nsection]]
            path = RayPath(sourceID, pathID)
            for isec in range(nsection):
                path.add_section(RayPathSection(*sections[isec*2:isec*2+2],
                                                vtypes[isec]))
            sources[-1].add_path(path)
    return(sources)

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
    vmodel = seispy.velocity.VelocityModel("%s/vgrids.in" % rootin, "fmm3d")
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
