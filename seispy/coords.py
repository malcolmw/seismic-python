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

    def toCartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        ρ = seispy.constants.EARTH_RADIUS - self[...,2]
        θ = π/2 - np.radians(self[...,0])
        φ = np.radians(self[...,1])
        cart[...,0] = ρ * np.sin(θ) * np.cos(φ)
        cart[...,1] = ρ * np.sin(θ) * np.sin(φ)
        cart[...,2] = ρ * np.cos(θ)
        return(cart)

    def toLeftSpherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = seispy.constants.EARTH_RADIUS - self[...,2]
        lspher[...,1] = np.radians(self[...,0])
        lspher[...,2] = np.radians(self[...,1])
        return(lspher)


    def toSpherical(self):
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


    def toGeographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        ρ = np.sqrt(np.sum(np.square(self),axis=-1))
        geo[...,0] = np.degrees(π/2 - np.arccos(self[...,2]/ρ))
        geo[...,1] = np.degrees(np.arctan2(self[...,1], self[...,0]))
        geo[...,2] = seispy.constants.EARTH_RADIUS - ρ
        return(geo)

    def toLeftSpherical(self):
        lspher = LeftSphericalCoordinates(self.shape[:-1])
        lspher[...,0] = np.sqrt(np.sum(np.square(self),axis=-1))
        lspher[...,1] = π/2 - np.arccos(self[...,2]/lspher[...,0])
        lspher[...,2] = np.arctan2(self[...,1], self[...,0])
        return(lspher)

    def toSpherical(self):
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
        if False in [ρ >= 0 for ρ in self[...,0].flatten()]:
            raise(ValueError("all values for ρ must satisfiy 0 <= ρ"))
        if False in  [0 <= θ <= π for θ in self[...,1].flatten()]:
            raise(ValueError("all values for θ must satisfiy 0 <= θ <= π"))
        if False in  [-π <= φ <= π for φ in self[...,2].flatten()]:
            raise(ValueError("all values for φ must satisfiy -π <= φ <= π"))

    def toCartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(self[...,1])
        return(cart)

    def toGeographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(π/2 - self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = seispy.constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def toLeftSpherical(self):
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
        if False in  [ρ < 0 for ρ in self[...,0].flatten()]:
            raise(ValueError("all values for ρ must satisfiy 0 <= ρ"))
        if False in  [-π/2 <= θ <= π/2 for θ in self[...,1].flatten()]:
            raise(ValueError("all values for λ must satisfiy -π/2 <= λ <= π/2"))
        if False in  [-π <= φ <= π for φ in self[...,2].flatten()]:
            raise(ValueError("all values for φ must satisfiy -π <= φ <= π"))

    def toCartesian(self):
        cart = CartesianCoordinates(self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(π/2 - self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(π/2 - self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(π/2 - self[...,1])
        return(cart)

    def toGeographic(self):
        geo = GeographicCoordinates(self.shape[:-1])
        geo[...,0] = np.degrees(self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = seispy.constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def toSpherical(self):
        spher = SphericalCoordinates(self.shape[:-1])
        spher[...,0] = self[...,0]
        spher[...,1] = π/2 - self[...,1]
        spher[...,2] = self[...,2]
        return(spher)

if __name__ == "__main__":
    print("coords.py not an executable script!!!")
    exit()
