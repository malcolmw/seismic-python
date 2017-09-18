"""
This module deprecates the geometry module.
"""
import numpy as np
import seispy

π = np.pi

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
        if False in [depth <= seispy.constants.EARTH_RADIUS
                     for depth in self[...,2].flatten()]:
            raise(ValueError("all depth values must satisfy depth <= "\
                    "{:f}".format(seispy.constants.EARTH_RADIUS)))

    def to_cartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        rho = seispy.constants.EARTH_RADIUS - self[...,2]
        theta = π/2 - np.radians(self[...,0])
        phi = np.radians(self[...,1])
        cart[...,0] = rho * np.sin(theta) * np.cos(phi)
        cart[...,1] = rho * np.sin(theta) * np.sin(phi)
        cart[...,2] = rho * np.cos(theta)
        return(cart)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = seispy.constants.EARTH_RADIUS - self[...,2]
        lspher[...,1] = np.radians(self[...,0])
        lspher[...,2] = np.radians(self[...,1])
        return(lspher)


    def to_spherical(self):
        spher = SphericalCoordinates(self.shape[:-1])
        spher[...,0] = seispy.constants.EARTH_RADIUS - self[...,2]
        spher[...,1] = np.radians(90 - self[...,0])
        spher[...,2] = np.radians(self[...,1])
        return(spher)


class CartesianCoordinates(np.ndarray):
    def __init__(self, args):
        self.resize(self.shape + (3,), refcheck=False)
        # Set all elements to 0
        self *= self*0

    def rotate(self, α, β, γ):
        """
        """
        R = np.asarray(np.matrix([[np.cos(α), -np.sin(α), 0],
                                  [np.sin(α), np.cos(α), 0],
                                  [0, 0, 1]])\
                     * np.matrix([[np.cos(β), 0, np.sin(β)],
                                  [0, 1, 0],
                                  [-np.sin(β), 0, np.cos(β)]])\
                     * np.matrix([[1, 0, 0],
                                  [0, np.cos(γ), -np.sin(γ)],
                                  [0, np.sin(γ), np.cos(γ)]]))
        return(np.dot(self, R))


    def to_geographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        rho = np.sqrt(np.sum(np.square(self),axis=-1))
        geo[...,0] = np.degrees(π/2 - np.arccos(self[...,2]/rho))
        geo[...,1] = np.degrees(np.arctan2(self[...,1], self[...,0]))
        geo[...,2] = seispy.constants.EARTH_RADIUS - rho
        return(geo)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = np.sqrt(np.sum(np.square(self),axis=-1))
        lspher[...,1] = π/2 - np.arccos(self[...,2]/lspher[...,0])
        lspher[...,2] = np.arctan2(self[...,1], self[...,0])
        return(lspher)

    def to_spherical(self):
        spher = SphericalCoordinates(self.shape[:-1])
        spher[...,0] = np.sqrt(np.sum(np.square(self),axis=-1))
        spher[...,1] = np.arccos(self[...,2]/spher[...,0])
        spher[...,2] = np.arctan2(self[...,1], self[...,0])
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
        if False in [rho >= 0 for rho in self[...,0].flatten()]:
            raise(ValueError("all values for rho must satisfiy 0 <= rho"))
        if False in  [0 <= theta <= π for theta in self[...,1].flatten()]:
            raise(ValueError("all values for theta must satisfiy 0 <= theta <= π"))
        if False in  [-π <= phi <= π for phi in self[...,2].flatten()]:
            raise(ValueError("all values for phi must satisfiy -π <= phi <= π"))

    def to_cartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(self[...,1])
        return(cart)

    def to_geographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(π/2 - self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = seispy.constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = self[...,0]
        lspher[...,1] = π/2  - self[...,1]
        lspher[...,2] = self[...,2]
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
        if False in  [rho >= 0 for rho in self[...,0].flatten()]:
            raise(ValueError("all values for rho must satisfiy 0 <= rho"))
        if False in  [-π/2 <= theta <= π/2 for theta in self[...,1].flatten()]:
            raise(ValueError("all values for lambda must satisfiy -π/2 <= lambda <= π/2"))
        if False in  [-π <= phi <= π for phi in self[...,2].flatten()]:
            raise(ValueError("all values for phi must satisfiy -π <= phi <= π"))

    def to_cartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(π/2 - self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(π/2 - self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(π/2 - self[...,1])
        return(cart)

    def to_geographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = seispy.constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def to_spherical(self):
        spher = SphericalCoordinates(self.shape[:-1])
        spher[...,0] = self[...,0]
        spher[...,1] = π/2 - self[...,1]
        spher[...,2] = self[...,2]
        return(spher)

def as_cartesian(array):
    array = np.asarray(array)
    cart = CartesianCoordinates(array.shape[:-1])
    cart[...] = array
    return(cart)

def as_geographic(array):
    array = np.asarray(array)
    geo = GeographicCoordinates(array.shape[:-1])
    geo[...] = array
    return(geo)

def as_left_spherical(array):
    array = np.asarray(array)
    lspher = LeftSphericalCoordinates(array.shape[:-1])
    lspher[...] = array
    return(lspher)

def as_spherical(array):
    array = np.asarray(array)
    spher = SphericalCoordinates(array.shape[:-1])
    spher[...] = array
    return(spher)

if __name__ == "__main__":
    print("coords.py not an executable script!!!")
    exit()
