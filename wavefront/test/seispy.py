import numpy as np
EARTH_RADIUS = 6371

π = np.pi

class GeoSurface(object):
    """
    A queryable container class to interpolate topographic data on a
    regular grid.
    """
    def __init__(self):
        pass

    def _callable(self, lat, lon):
# HACK
# THIS NEEDS TO BE CLEANED UP
        #lon = lon % 360 - 360
        _, θ, φ = as_geographic([lat, lon, 0]).to_spherical()
        iθ = (θ - self.grid.θ0) / self.grid.dθ
        iθ0 = int(min([max([0, np.floor(iθ)]), self.grid.nθ - 1]))
        iθ1 = int(max([0, min([self.grid.nθ-1, np.ceil(iθ)])]))
        iφ = (φ - self.grid.φ0) / self.grid.dφ
        iφ0 = int(min([max([0, np.floor(iφ)]), self.grid.nφ - 1]))
        iφ1 = int(max([0, min([self.grid.nφ, np.ceil(iφ)])]))
        R00 = self.coordinates[iθ0, iφ0, 0]
        R01 = self.coordinates[iθ0, iφ1, 0]
        R10 = self.coordinates[iθ1, iφ0, 0]
        R11 = self.coordinates[iθ1, iφ1, 0]
        dθ = θ - self.coordinates[iθ0, iφ0, 1]
        dφ = φ - self.coordinates[iθ0, iφ0, 2]
        R0 = R00 + (R10 - R00) * dθ
        R1 = R01 + (R11 - R01) * dθ
        return(R0 + (R1 - R0) * dφ)

    def read(self, infile):
        infile = open(infile)
        LAT, LON, DEPTH = [], [], []
        COORDINATES = np.empty((0, 3))
        for line in infile:
            COORDINATES = np.append(COORDINATES,
                                    [[float(v) for v in line.split()]],
                                    axis=0)
        COORDINATES[:,2] *= -1/1000
        COORDINATES[:,[0,1]] = COORDINATES[:,[1,0]]
        COORDINATES = as_geographic(COORDINATES)
        nlat = len(np.unique(COORDINATES[:,0]))
        nlon = len(np.unique(COORDINATES[:,1]))
        minlat = COORDINATES[:,0].min()
        minlon = COORDINATES[:,1].min()
        maxlat = COORDINATES[:,0].max()
        maxlon = COORDINATES[:,1].max()
        dlat = (maxlat - minlat) / (nlat - 1)
        dlon = (maxlon - minlon) / (nlon - 1)
        self.grid = GeoGrid2D(minlat, minlon, nlat, nlon, dlat, dlon)
        COORDINATES = COORDINATES.to_spherical()
        COORDINATES = np.array(sorted(COORDINATES, key=lambda c: (c[1], c[2])))
        COORDINATES = COORDINATES.reshape((nlat, nlon, 3))
        self.coordinates = COORDINATES


    def __call__(self, lat, lon):
        return(self._callable(lat, lon))

class GeoGrid2D(object):
    def __init__(self, lat0, lon0, nlat, nlon, dlat, dlon):
# NOTE: Origin of spherical coordinate system and geographic coordinate
# system is not the same!
# Geographic coordinate system
        self.lat0, self.lon0, _ = as_geographic([lat0, lon0, 0])
        self.nlat, self.nlon = nlat, nlon
        self.dlat, self.dlon = dlat, dlon
# Spherical/Pseudospherical coordinate systems
        self.nθ = self.nλ = self.nlat
        self.nφ = self.nlon

        self.dθ = self.dλ = np.radians(self.dlat)
        self.dφ = np.radians(self.dlon)

        self.λ0 = np.radians(self.lat0)
        self.θ0 = np.pi/2 - (self.λ0 + (self.nλ - 1) * self.dλ)
        self.φ0 = np.radians(self.lon0)

    def __str__(self):
        s = "lat0, lon0: {:.15g}, {:.15g}\n".format(self.lat0,
                                                    self.lon0)
        s += "nlat, nlon: {:8d}, {:8d}\n".format(self.nlat,
                                                 self.nlon)
        s += "dlat, dlon: {:.15g}, {:.15g}\n".format(self.dlat,
                                                     self.dlon)
        s += "θ0, λ0, φ0: {:.15g}, {:.15g}, {:.15g}\n".format(self.θ0,
                                                             self.λ0,
                                                             self.φ0)
        s += "nθ, nλ, nφ : {:8d}, {:8d}\n".format(self.nθ,
                                                  self.nλ,
                                                  self.nφ)
        s += "dθ, dλ, dφ : {:.15g}, {:.15g}, {:.15g}".format(self.dθ,
                                                             self.dλ,
                                                             self.dφ)
        return(s)

class GeoGrid3D(object):
    def __init__(self, lat0, lon0, depth0, nlat, nlon, ndepth, dlat, dlon, ddepth):
# NOTE: Origin of spherical coordinate system and geographic coordinate
# system is not the same!
# Geographic coordinate system
        self.lat0, self.lon0, self.depth0 =\
                as_geographic([lat0, lon0, depth0])
        self.nlat, self.nlon, self.ndepth = nlat, nlon, ndepth
        self.dlat, self.dlon, self.ddepth = dlat, dlon, ddepth
# Spherical/Pseudospherical coordinate systems
        self.nρ = self.ndepth
        self.nθ = self.nλ = self.nlat
        self.nφ = self.nlon
        self.dρ = self.ddepth
        self.dθ = self.dλ = np.radians(self.dlat)
        self.dφ = np.radians(self.dlon)
        self.ρ0 = EARTH_RADIUS\
                - (self.depth0 + (self.ndepth - 1) * self.ddepth)
        self.λ0 = np.radians(self.lat0)
        self.θ0 = π/2 - (self.λ0 + (self.nλ - 1) * self.dλ)
        self.φ0 = np.radians(self.lon0)

    def fit_subgrid(self,
                    nρ=None,
                    nlat=None,
                    nlon=None):
        nρ = self.nρ if nρ is None else nρ
        nlat = self.nθ if nlat is None else nlat
        nlon = self.nφ if nlon is None else nlon

        ρ0 = self.ρ0 + self.dρ * 1.01
        ρmax = self.ρ0 + (self.nρ - 2.01) * self.dρ
        dρ = (ρmax - ρ0) / (nρ - 1)

        lat0 = self.lat0 + 1.01 * self.dlat
        latmax = self.lat0 + (self.nlat - 2.01) * self.dlat
        dlat = (latmax - lat0) / (nlat - 1)

        lon0 = self.lon0 + self.dlon * 1.01
        lonmax = self.lon0 + (self.nlon - 2.01) * self.dlon
        dlon = (lonmax - lon0) / (nlon - 1)

        return(GeoGrid3D(lat0, lon0, EARTH_RADIUS - ρmax,
                         nlat, nlon, nρ, dlat, dlon, dρ))

class GeographicCoordinates(np.ndarray):
    def __init__(self, args):
        self.resize(self.shape + (3,), refcheck=False)
        # Set all elements to 0
        self *= self*0
        self[np.where(np.isnan(self))] = 0


    def __setitem__(self, index, coordinates):
        coordinates = np.asarray(coordinates)
        if coordinates.shape == (3,):
            coordinates = np.asarray([coordinates])
        super().__setitem__(index, coordinates)
        if False in  [-90 <= lat <= 90 for lat in self[...,0].flatten()]:
            raise(ValueError("all values for latitude must satisfiy -90 "\
                    "<= latitude <= 90"))
        if False in  [-180 <= lon <= 180 for lon in self[...,1].flatten()]:
            raise(ValueError("all values for longitude must satisfiy -180 <= "\
                    "longitude <= 180"))
        if False in [depth <= EARTH_RADIUS
                     for depth in self[...,2].flatten()]:
            raise(ValueError("all depth values must satisfy depth <= "\
                    "{:f}".format(EARTH_RADIUS)))

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = EARTH_RADIUS - self[...,2]
        lspher[...,1] = np.radians(self[...,0])
        lspher[...,2] = np.radians(self[...,1])
        return(lspher)

class  LeftSphericalCoordinates(np.ndarray):
    def __init__(self, args):
        self.resize(self.shape + (3,), refcheck=False)
        # Set all elements to 0.
        self *= self*0
        self[np.where(np.isnan(self))] = 0

    def __setitem__(self, index, coordinates):
        coordinates = np.asarray(coordinates)
        if coordinates.shape == (3,):
            coordinates = np.asarray([coordinates])
        super().__setitem__(index, coordinates)
        if False in  [ρ >= 0 for ρ in self[...,0].flatten()]:
            raise(ValueError("all values for ρ must satisfiy 0 <= ρ"))
        if False in  [-π/2 <= θ <= π/2 for θ in self[...,1].flatten()]:
            raise(ValueError("all values for λ must satisfiy -π/2 <= λ <= π/2"))
        if False in  [-π <= φ <= π for φ in self[...,2].flatten()]:
            raise(ValueError("all values for φ must satisfiy -π <= φ <= π"))

    def to_geographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = EARTH_RADIUS - self[...,0]
        return(geo)

    def to_spherical(self):
        spher = SphericalCoordinates(self.shape[:-1])
        spher[...,0] = self[...,0]
        spher[...,1] = π/2 - self[...,1]
        spher[...,2] = self[...,2]
        return(spher)

class SphericalCoordinates(np.ndarray):
    def __init__(self, args):
        self.resize(self.shape + (3,), refcheck=False)
        # Set all elements to 0
        self *= self*0
        self[np.where(np.isnan(self))] = 0

    def __setitem__(self, index, coordinates):
        coordinates = np.asarray(coordinates)
        if coordinates.shape == (3,):
            coordinates = np.asarray([coordinates])
        super().__setitem__(index, coordinates)
        if False in [ρ >= 0 for ρ in self[...,0].flatten()]:
            raise(ValueError("all values for ρ must satisfiy 0 <= ρ"))
        if False in  [0 <= θ <= π for θ in self[...,1].flatten()]:
            raise(ValueError("all values for θ must satisfiy 0 <= θ <= π"))
        if False in  [-π <= φ <= π for φ in self[...,2].flatten()]:
            raise(ValueError("all values for φ must satisfiy -π <= φ <= π"))

    def to_geographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(π/2 - self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = EARTH_RADIUS - self[...,0]
        return(geo)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = self[...,0]
        lspher[...,1] = π/2  - self[...,1]
        lspher[...,2] = self[...,2]
        return(lspher)

def as_left_spherical(array):
    array = np.asarray(array)
    lspher = LeftSphericalCoordinates(array.shape[:-1])
    lspher[...] = array
    return(lspher)

def as_geographic(array):
    array = np.asarray(array)
    geo = GeographicCoordinates(array.shape[:-1])
    geo[...] = array
    return(geo)

def read_interfaces(infile):
    infile = open(infile)
    ninter = int(infile.readline().split()[0])
    nλ, nφ = [int(v) for v in infile.readline().split()[:2]]
    dλ, dφ = [np.float64(v) for v in infile.readline().split()[:2]]
    λ0, φ0 = [np.float64(v) for v in infile.readline().split()[:2]]
    grid = GeoGrid2D(np.degrees(λ0), np.degrees(φ0),
                     nλ, nφ,
                     np.degrees(dλ), np.degrees(dφ))
    interfaces = []
    for iinter in range(ninter):
        surf = GeoSurface()
        surf.grid = grid
        coordinates = as_left_spherical([[[np.float64(infile.readline().split()[0]),
                                                  λ0 + iλ*dλ,
                                                  φ0 + iφ*dφ]
                                                for iφ in range(nφ)]
                                                for iλ in range(nλ)])
        coordinates = np.flip(coordinates.to_spherical(), axis=0)
        surf.coordinates = coordinates
        interfaces.append(surf)
    return(interfaces)

def read_vgrids(inf):
    inf = open(inf, "r")
    nvgrids, nvtypes = [int(v) for v in inf.readline().split()[:2]]
    v_type_grids = {"n_vgrids": nvgrids, "n_vtypes": nvtypes}
    for (typeID, gridID) in [(ivt, ivg) for ivt in range(1, nvtypes+1)
                                        for ivg in range(1, nvgrids+1)]:
        if typeID not in v_type_grids:
            v_type_grids[typeID] = {}
        model = {"typeID": typeID, "gridID": gridID}
        nρ, nλ, nφ = [int(v) for v in inf.readline().split()[:3]]
        dρ, dλ, dφ = [float(v) for v in inf.readline().split()[:3]]
        ρ0, λ0, φ0 = [float(v) for v in inf.readline().split()[:3]]
        model["grid"] = GeoGrid3D(np.degrees(λ0),
                                  np.degrees(φ0),
                                  EARTH_RADIUS - (ρ0 + (nρ-1)*dρ),
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
        v_type_grids[typeID][gridID] = model
    return(v_type_grids)
