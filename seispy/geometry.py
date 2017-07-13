"""
This module provides basic geometric utility functions to facilitate
working in differenct coordinate systems.

Coordinate systems

SPHERICAL
=========
Spherical coordinates are defined relative to the cartesian coordanets
as:
r - radial distance to point from origin
theta - polar angle [0, pi]
phi - azimuthal angle 2 * pi]

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
                 radians,\
                 sin,\
                 sqrt
import numpy as np
from obspy.geodetics.base import gps2dist_azimuth
import seispy


EARTH_RADIUS = seispy.constants.EARTH_RADIUS


def geo2sph(lat, lon, z):
    """
    Convert geographic coordinates to spherical coordinates.
    Returns r, theta, phi.
    """
    if not (-90. <= lat <= 90.) or not (-180. < lon < 360.):
        raise ValueError("invalid geographic coordinates")
    lon %= 360.
    theta = radians(90. - lat)
    phi = radians(lon)
    r = EARTH_RADIUS - z
    return r, theta, phi


def azimuth(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return((90 - degrees(atan2(y2 - y1, x2 - x1))) % 360)


def distance(u, v):
    if len(u) != len(v):
        raise(ValueError("vectors u and v must have same length"))
    u = np.asarray(u)
    v = np.asarray(v)
    return(sqrt(sum((u - v) ** 2)))


def get_line_endpoints(lat0, lon0, az, length):
    phi = radians(az % 360)
    l2 = 0.5 * length / 111
    theta1 = -phi + pi/2
    theta2 = -phi - pi/2
    return((lon0 + l2 * cos(theta2), lat0 + l2 * sin(theta2)),
           (lon0 + l2 * cos(theta1), lat0 + l2 * sin(theta1)))


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


def quadrant_coverage(source, receivers):
    q1, q2, q3, q4 = False, False, False, False
    lon0, lat0 = source.lon, source.lat
    for rx in receivers:
        rlon, rlat = rx.lon, rx.lat
        if lat0 < rlat and lon0 < rlon:
            q1 = True
        elif lat0 < rlat and rlon < lon0:
            q2 = True
        elif rlat < lat0 and rlon < lon0:
            q3 = True
        elif rlat < lat0 and lon0 < rlon:
            q4 = True
    coverage = 0.0
    for q in q1, q2, q3, q4:
        if q:
            coverage += 1.0
    return coverage / 4.0


class Vector(np.ndarray):

    def __new__(cls, v):
        u = np.ndarray.__new__(cls, len(v))
        for i in range(len(v)):
            u[i] = v[i]
        return u

    def rotate(self, axis, theta):
        return self.__new__(self.__class__,
                            rotation_matrix(axis, theta).dot(self))

    def translate(self, v):
        u = self.__new__(self.__class__, [0 for i in range(len(v))])
        for i in range(len(v)):
            u[i] = self[i] - v[i]
        return u
