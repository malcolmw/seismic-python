import numpy as np
from . import constants as _constants

PI = np.pi


class GeographicCoordinates(np.ndarray):
    """
    This class provides a container for geographic coordinates and
    methods to transform the coordinates to other commonly used
    systems.
    This class does not support creation via the np.ndarray.view
    mechanism.
    """
    def __new__(cls, *args):
        """
        This creates a new instance of GeographicCoordinates, makes sure
        that the last dimesion is of length 3, and sets all elements
        to 0.
        """
        return(np.zeros(args + (3,)).view(GeographicCoordinates))

    def __setitem__(self, index, value):
        """
        This sets the values of the array and tests that they are in
        meaningful ranges.
        """
        super().__setitem__(index, value)
        if not np.all((-90 <= self[...,0]) & (self[...,0] <= 90)):
            raise(ValueError("all values for latitude must satisfiy -90 "\
                    "<= latitude <= 90"))
        if not np.all((-180 <= self[...,1]) & ( self[...,1] <= 180)):
            raise(ValueError("all values for longitude must satisfiy -180 <= "\
                    "longitude <= 180"))
        if not np.all(self[...,2] <= _constants.EARTH_RADIUS):
            raise(ValueError("all depth values must satisfy depth <= "\
                    "{:f}".format(_constants.EARTH_RADIUS)))

    def to_cartesian(self):
        cart = CartesianCoordinates(*self.shape[:-1])
        rho = np.asarray(_constants.EARTH_RADIUS - self[...,2])
        theta = np.asarray(PI/2 - np.radians(self[...,0]))
        phi = np.asarray(np.radians(self[...,1]))
        cart[...,0] = rho * np.sin(theta) * np.cos(phi)
        cart[...,1] = rho * np.sin(theta) * np.sin(phi)
        cart[...,2] = rho * np.cos(theta)
        return(cart)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(*self.shape[:-1])
        lspher[...,0] = _constants.EARTH_RADIUS - self[...,2]
        lspher[...,1] = np.radians(self[...,0])
        lspher[...,2] = np.radians(self[...,1])
        return(lspher)

    def to_ned(self, origin=None):
        if origin is None:
            origin = GeographicCoordinates(1)[0]
        return(self.to_cartesian().to_ned(origin=origin))

    def to_spherical(self):
        spher = SphericalCoordinates(*self.shape[:-1])
        spher[...,0] = _constants.EARTH_RADIUS - self[...,2]
        spher[...,1] = np.radians(90 - self[...,0])
        spher[...,2] = np.radians(self[...,1])
        return(spher)


class CartesianCoordinates(np.ndarray):
    """
    This class provides a container for Cartesian coordinates and
    methods to transform the coordinates to other commonly used
    systems.
    This class does not support creation via the np.ndarray.view
    mechanism.
    """
    def __new__(cls, *args):
        """
        This creates a new instance of CartesianCoordinates, makes sure
        that the last dimesion is of length 3, and sets all elements
        to 0.
        """
        return(np.zeros(args + (3,)).view(CartesianCoordinates))

    def rotate(self, *args):
        """
        Rotates a set of cartesian coordinates by alpha radians about
        the z-axis, then beta radians about the y'-axis and then
        gamma radians about the z''-axis.
        """
        return(self.dot(rotation_matrix(*args)))


    def to_geographic(self):
        geo = GeographicCoordinates(*self.shape[:-1])
        rho = np.sqrt(np.sum(np.square(self),axis=-1))
        geo[...,0] = np.degrees(PI/2 - np.arccos(self[...,2]/rho))
        geo[...,1] = np.degrees(np.arctan2(self[...,1], self[...,0]))
        geo[...,2] = _constants.EARTH_RADIUS - rho
        return(geo)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(*self.shape[:-1])
        lspher[...,0] = np.sqrt(np.sum(np.square(self),axis=-1))
        lspher[...,1] = PI/2 - np.arccos(self[...,2]/lspher[...,0])
        lspher[...,2] = np.arctan2(self[...,1], self[...,0])
        return(lspher)

    def to_ned(self, origin=GeographicCoordinates(1)[0]):
        theta0 = np.radians(90-origin[0])
        phi0 = np.radians(origin[1])
        rho0 = _constants.EARTH_RADIUS-origin[2]
        # This creates XYZ/NEZ coordinates
        ned = self.rotate(phi0, theta0, np.pi/2).view(NEDCoordinates)
        # Swap X and Y axes
        ned[..., [0,1]] = ned[..., [1,0]]
        # Map Z to Down
        ned[..., 2] = rho0 - ned[..., 2]
        # Set the origin of the NEDCoordinates object
        ned.set_origin(origin)
        return(ned)

    def to_spherical(self):
        spher = SphericalCoordinates(*self.shape[:-1])
        spher[...,0] = np.sqrt(np.sum(np.square(self),axis=-1))
        spher[...,1] = np.arccos(self[...,2]/spher[...,0])
        spher[...,2] = np.arctan2(self[...,1], self[...,0])
        return(spher)

class NEDCoordinates(CartesianCoordinates):
    """
    This class provides a container for North-East-Down coordinates and
    methods to transform the coordinates to other commonly used
    systems.
    This class does not support creation via the np.ndarray.view
    mechanism.
    """
    def __new__(cls, *args, **kwargs):
        """
        This creates a new instance of NEDCoordinates, makes sure
        that the last dimesion is of length 3, and sets all elements
        to 0.
        """
        instance = np.zeros(args + (3,)).view(NEDCoordinates)
        if "origin" in kwargs:
            instance.set_origin(kwargs["origin"])
        return(instance)

    def rotate(self, *args):
        rot = super().rotate(*args).view(NEDCoordinates)
        rot.origin = self.origin
        return(rot)


    def set_origin(self, origin):
        if isinstance(origin, GeographicCoordinates):
            self.origin = origin
        else:
            raise(NotImplementedError("NEDCoordinates can only handle "
                                      "GeographicCoordinates right now"))

    def to_cartesian(self):
        theta0 = np.radians(90-self.origin[0])
        phi0 = np.radians(self.origin[1])
        rho0 = _constants.EARTH_RADIUS-self.origin[2]
        cart = self.view(CartesianCoordinates)
        # Map Down to Z
        cart[..., 2] = rho0 - cart[..., 2]
        # Swap X and Y axes
        cart[..., [0,1]] = cart[..., [1,0]]
        # This creates XYZ/NEZ coordinates
        return(cart.rotate(-np.pi/2, -theta0, -phi0))

    def to_geographic(self):
        return(self.to_cartesian().to_geographic())

class SphericalCoordinates(np.ndarray):
    """
    This class provides a container for spherical coordinates and
    methods to transform the coordinates to other commonly used
    systems.
    This class does not support creation via the np.ndarray.view
    mechanism.
    """
    def __new__(cls, *args):
        """
        This creates a new instance of SphericalCoordinates, makes sure
        that the last dimesion is of length 3, and sets all elements
        to 0.
        """
        return(np.zeros(args + (3,)).view(SphericalCoordinates))

    def __setitem__(self, index, value):
        """
        This sets the values of the array and tests that they are in
        meaningful ranges.
        """
        super().__setitem__(index, value)
        if not np.all(0 <= self[...,0]):
            raise(ValueError("all values for rho must satisfiy 0 <= rho"))
        if not np.all((0 <= self[...,1]) & (self[...,1] <= PI)):
            raise(ValueError("all values for theta must satisfiy 0 <= theta <= π"))
        if not np.all((-PI <= self[...,2]) & (self[...,2] <= PI)):
            raise(ValueError("all values for phi must satisfiy -π <= phi <= π"))

    def to_cartesian(self):
        cart = CartesianCoordinates(*self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(self[...,1])
        return(cart)

    def to_geographic(self):
        geo = GeographicCoordinates(*self.shape[:-1])
        geo[...,0] = np.degrees(PI/2 - self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = _constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def to_left_spherical(self):
        lspher = LeftSphericalCoordinates(*self.shape[:-1])
        lspher[...,0] = self[...,0]
        lspher[...,1] = PI/2  - self[...,1]
        lspher[...,2] = self[...,2]
        return(lspher)


class  LeftSphericalCoordinates(np.ndarray):
    """
    This class provides a container for spherical coordinates and
    methods to transform the coordinates to other commonly used
    systems.
    This class does not support creation via the np.ndarray.view
    mechanism.
    """
    def __new__(cls, *args):
        """
        This creates a new instance of SphericalCoordinates, makes sure
        that the last dimesion is of length 3, and sets all elements
        to 0.
        """
        return(np.zeros(args + (3,)).view(LeftSphericalCoordinates))

    def __setitem__(self, index, value):
        """
        This sets the values of the array and tests that they are in
        meaningful ranges.
        """
        super().__setitem__(index, value)
        if not np.all(0 <= self[...,0]):
            raise(ValueError("all values for rho must satisfiy 0 <= rho"))
        if not np.all((-PI/2 <= self[...,1]) & (self[...,1] <= PI/2)):
            raise(ValueError("all values for theta must satisfiy -π/2 <= theta <= π/2"))
        if not np.all((-PI <= self[...,2]) & (self[...,2] <= PI)):
            raise(ValueError("all values for phi must satisfiy -π <= phi <= π"))

    def to_cartesian(self):
        cart = CartesianCoordinates(*self.shape[:-1])
        cart[...,0] = self[...,0]*np.sin(PI/2 - self[...,1])*np.cos(self[...,2])
        cart[...,1] = self[...,0]*np.sin(PI/2 - self[...,1])*np.sin(self[...,2])
        cart[...,2] = self[...,0]*np.cos(PI/2 - self[...,1])
        return(cart)

    def to_geographic(self):
        geo = GeographicCoordinates(*self.shape[:-1])
        geo[...,0] = np.degrees(self[...,1])
        geo[...,1] = np.degrees(self[...,2])
        geo[...,2] = _constants.EARTH_RADIUS - self[...,0]
        return(geo)

    def to_spherical(self):
        spher = SphericalCoordinates(*self.shape[:-1])
        spher[...,0] = self[...,0]
        spher[...,1] = PI/2 - self[...,1]
        spher[...,2] = self[...,2]
        return(spher)


def rotation_matrix(*args):
    """
    Return the rotation matrix used to rotate a set of cartesian
    coordinates by alpha radians about the z-axis, then beta radians
    about the y'-axis and then gamma radians about the z''-axis.
    """
    if len(args) == 1:
        alpha, beta, gamma = args[0], 0, 0
    elif len(args) == 3:
        alpha, beta, gamma = args
    else:
        raise(ValueError("number of positional arguments must be 1 or 3"))
    ALPHA = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                        [np.sin(alpha), np.cos(alpha), 0],
                        [0, 0, 1]])
    BETA = np.array([[np.cos(beta), 0, np.sin(beta)],
                        [0, 1, 0],
                        [-np.sin(beta), 0, np.cos(beta)]])
    GAMMA = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                        [np.sin(gamma), np.cos(gamma), 0],
                        [0, 0, 1]])
    R = ALPHA.dot(BETA).dot(GAMMA)
    return(R)

def as_cartesian(array):
    cart = CartesianCoordinates(*np.asarray(array).shape[:-1])
    cart[...] = array
    return(cart)

def as_geographic(array):
    geo = GeographicCoordinates(*np.asarray(array).shape[:-1])
    geo[...] = array
    return(geo)

def as_left_spherical(array):
    lspher = LeftSphericalCoordinates(*np.asarray(array).shape[:-1])
    lspher[...] = array
    return(lspher)

def as_ned(array, origin=None):
    ned = NEDCoordinates(*np.asarray(array).shape[:-1])
    if origin is not None:
        ned.set_origin(origin)
    ned[...] = array
    return(ned)

def as_spherical(array):
    spher = SphericalCoordinates(*np.asarray(array).shape[:-1])
    spher[...] = array
    return(spher)

def test():
    with open("/Users/malcolcw/Projects/Shared/Topography/anza.xyz") as inf:
        data = np.array([[float(v) for v in line.split()] for line in inf])
        gc = GeographicCoordinates(len(data))
        gc[:,0], gc[:,1], gc[:,2] = data[:,1], data[:,0], data[:,2]/1000
        print(gc.to_cartesian())
        #np.save("topo.npy", gc.to_cartesian().rotate(P0, T0, 0))

if __name__ == "__main__":
    print("coords.py not an executable script!!!")
    test()
    exit()
