"""
This module provides basic geometric utility functions to facilitate
working in different coordinate systems.
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


def azimuth(lat1, lon1, lat2, lon2):
    """
    Return the azimuth of the line connecting points **(lat1, lon1)**
    and **(x2, y2)**.

    :param float lat1: latitude coordinate of point 1
    :param float lon1: longitude coordinate of point 1
    :param float lat2: latitude coordinate of point 2
    :param float lon2: longitude coordinate of point 2
    :returns: azimuth of the line connecting points **(lat1, lon1)**
              and **(lat2, lon2)** **{Units:** degrees, **Range:** [0,
              360)}.
    :rtype: float
    """
    return((90 - degrees(atan2(lat2 - lat1, lon2 - lon1))) % 360)


def azimuth2radians(azimuth):
    """
    Convert azimuth value (measured clockwise from North in degrees) to
    a value measured in radians counter-clockwise from East.

    :param float azimuth: azimuth in degrees
    :returns: equivalent of azimuth in radians
    :rtype: float
    """
    return(pi/2 - radians(azimuth))


def az2rad(azimuth):
    """
    Convenience wrapper of :func:`azimuth2radians`.
    """
    return(azimuth2radians(azimuth))


def coordinates(lat0, lon0, azimuth, distance):
    """
    Return coordinates of point **distance** degrees from
    (**lat0**, **lon0**) along **azimuth**.

    :param float lat0: latitude of starting point
    :param float lon0: longitude of starting point
    :param float azimuth: azimuth of path to traverse **{Units:**
                          *Degrees*, **Range:** *(-inf, inf)*\ **}**
    :param float distance: distance along path to traverse **{Units**:
                           *Degrees*\ **}**
    :returns: geographic coordinates **distance** degrees from
              (**lat0**, **lon0**) along **azimuth**
    :rtype: (float, float)
    :raises ValueError: if resulting coordinates are invalid
    """
    phi = az2rad(azimuth)
    dlat = sin(phi) * distance
    dlon = cos(phi) * distance
    lat, lon = lat0+dlat, lon0+dlon
    validate_geographic_coords(lat, lon)
    return(lat, lon)


def distance(u, v):
    """
    Return the Euclidean distance between vectors **u** and **v**.

    :param u: Vector 1.
    :type u: list, tuple or other iterable
    :param v: Vector 2.
    :type v: list, tuple or other iterable
    :returns: Euclidean distance between vectors **u** and **v**
    :rtype: float
    """
    if len(u) != len(v):
        raise(ValueError("vectors u and v must have same length"))
    u = np.asarray(u)
    v = np.asarray(v)
    return(sqrt(sum((u - v) ** 2)))


def get_line_endpoints(lat0, lon0, azimuth, length):
    """
    Return the geographic coordinates (latitude, longitude) of a length=\
    **length** line passing through coordinates **lat0** **lon0** with
    strike=\ **strike**.

    :param float lat0: latitude coordinate of line center {**Units**:
                       degrees, **Range**: [-90, 90]}
    :param float lon0: longitude coordinate of line center {**Units**:
                       degrees, **Range**: [-180, 360]}
    :param float azimuth: azimuth of line {**Units**: degrees,
                          **Range**: [0, 360]}
    :param float length: length of line **{Units:** *degrees*\ **}**
    :returns: geographic coordinates of length=\ **length** line
              passing through (**lat0**, **lon0**) with strike=
              **strike**
    :rtype: ((float, float), (float, float))
    """
    phi = radians(azimuth % 360)
    l2 = 0.5 * length
    theta1 = -phi + pi/2
    theta2 = -phi - pi/2
    return((lon0 + l2 * cos(theta2), lat0 + l2 * sin(theta2)),
           (lon0 + l2 * cos(theta1), lat0 + l2 * sin(theta1)))


def geo2sph(lat, lon, z):
    """
    Convert geographic coordinates to spherical coordinates.

    :param float lat: latitude coordinate {**Units**: degrees,
                      **Range**: [-90, 90]}
    :param float lon: longitude coordinate {**Units**: degrees,
                      **Range**: [-180, 360]}
    :param float depth: depth from surface {**Units**: km,
                        **Range**: (-inf, inf)}
    :returns: spherical coordinate conversion *(r, theta, phi)* of
              geographic coordinates
    :rtype: (float, float, float)
    """
    if not (-90. <= lat <= 90.) or not (-180. < lon < 360.):
        raise ValueError("invalid geographic coordinates")
    lon %= 360.
    theta = radians(90. - lat)
    phi = radians(lon)
    r = EARTH_RADIUS - z
    return r, theta, phi


def radians2azimuth(theta):
    """
    Convert value in radians measured counter-clockwise from East to
    azimuth value measured in degrees clockwise from North.

    :param float theta: value in radians measured clockwise from East
    :returns: azimuth equivalent of **theta** measured in degrees
              clockwise from North
    :rtype: float
    """
    return(degrees(pi/2 - theta))


def rad2az(theta):
    """
    Convenience wrapper for :func:`radians2azimuth`.
    """
    return(radians2azimuth(theta))


def sph2geo(r, theta, phi):
    """
    Convert spherical coordinates to geographic coordinates.

    :param float r: radial distance from coordinate system origin
                    {**Units**: km, **Range**: [0, inf)}
    :param float theta: polar angle {**Units**: radians, **Range**: [0,
                        pi]}
    :param float phi: azimuthal angle {**Units**: radians, **Range**:
                      [0, 2*pi]}
    :returns: geographic coordinate conversion *(lat, lon, depth)* of
              spherical coordinates
    :rtype: (float, float, float)
    """
    z = EARTH_RADIUS - r
    lat = 90 - degrees(theta)
    lon = degrees(phi)
    lon %= 360.
    return lat, lon, z


def sph2xyz(r, theta, phi):
    """
    Convert spherical coordinates to cartesian coordinates.

    :param float r: radial distance from coordinate system origin
                    {**Units**: km, **Range**: [0, inf)}
    :param float theta: polar angle {**Units**: radians, **Range**: [0,
                        pi]}
    :param float phi: azimuthal angle {**Units**: radians, **Range**:
                      [0, 2*pi]}
    :returns: cartesian coordinate conversion *(x, y, z)* of spherical
              coordinates
    :rtype: (float, float, float)
    """
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return x, y, z


def xyz2sph(x, y, z):
    """
    Convert cartesian coordinates to spherical coordinates.

    :param float x: cartesian x-coordinate {**Units**: km, **Range**:
                    [0, inf)}
    :param float y: cartesian y-coordinate {**Units**: km, **Range**:
                    [0, inf)}
    :param float z: cartesian z-coordinate {**Units**: km, **Range**:
                    [0, inf)}
    :returns: spherical coordinate conversion *(r, theta, phi)* of
              cartesian coordinates
    :rtype: (float, float, float)
    """
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = acos(z / r)
    phi = atan2(y, x)
    return r, theta, phi


def rotation_matrix(axis, theta):
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


def validate_geographic_coords(lat, lon):
    if not -90 <= lat <= 90:
        raise(ValueError("latitude must be in range [-90, 90]: %f" % lat))
    if not -180 <= lon < 360:
        raise(ValueError("longitude must be in range [-180, 360): %f" % lon))
