"""
This module provides basic geometric utility functions to facilitate
working in differenct coordinate systems.

Coordinate systems

SPHERICAL
=========
Spherical coordinates are defined relative to the cartesian coordanets
as:
r - radial distance to point from origin
theta - angular distance from z-axis to radial-axis [0, pi]
phi - angular distance from x-axis to raidal-axis [0, 2 * pi]

GEOGRAPHICAL
============
Geographical coordinates are assumed to be in degrees and are defined
as:
lat - latitude [90, -90]
lon - longitude [0, 360)
z - depth from surface

CARTESIAN
=========
Let's align our cartesian coordinates so the x-axis corresponds to the
lon = 0 axis and the z-axis aligns with North pole lat=90.
"""
from math import acos,\
                 atan2,\
                 cos,\
                 degrees,\
                 pi,\
                 sin,\
                 sqrt
import numpy as np

EARTH_RADIUS = 6371.

rad2deg = lambda phi: phi * (180. / pi)

deg2rad = lambda theta: theta * (pi / 180.)

def geo2sph(lat, lon, z):
    """
    Convert geographic coordinates to spherical coordinates.
    Returns r, theta, phi.
    """
    if not (-90. <= lat <= 90.) or not (-180. < lon < 360.):
        raise ValueError("invalid geographic coordinates")
    lon %= 360.
    theta = deg2rad(90. - lat)
    phi = deg2rad(lon)
    r = EARTH_RADIUS - z
    return r, theta, phi

def sph2geo(r, theta, phi):
    z = EARTH_RADIUS - r
    lat = 90 - degrees(theta)
    lon = degrees(phi)
    lon %= 360.
    return lat, lon, z

def sph2xyz(r, theta, phi):
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return x, y, z

def xyz2sph(x, y, z):
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = acos(z / r)
    phi = atan2(y, x)
    return r, theta, phi

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    if axis == 1 or axis == 'x' or axis == 'X':
        return np.array([[1, 0, 0],
                         [0, cos(theta), -sin(theta)],
                         [0, sin(theta), cos(theta)]])
    elif axis == 2 or axis == 'y' or axis == 'Y':
        return np.array([[cos(theta), 0, sin(theta)],
                         [0, 1, 0],
                         [-sin(theta), 0, cos(theta)]])
    elif axis == 3 or axis == 'z' or axis == 'Z':
        return np.array([[cos(theta), -sin(theta), 0],
                         [sin(theta), cos(theta), 0],
                         [0, 0, 1]])
    else:
        raise ValueError("invalid axis")

class Vector(np.ndarray):

    def __new__(cls, v):
        u = np.ndarray.__new__(cls, len(v))
        for i in range(len(v)):
            u[i] = v[i]
        return u

    def rotate(self, axis, theta):
        return self.__new__(self.__class__, rotation_matrix(axis, theta).dot(self))

    def translate(self, v):
        u = self.__new__(self.__class__, [0 for i in range(len(v))])
        for i in range(len(v)):
            u[i] = self[i] - v[i]
        return u
