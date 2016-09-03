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
lon - longitude [-180, 180]
z - depth from surface

CARTESIAN
=========
Let's align our cartesian coordinates so the x-axis corresponds to the
lon = 0 axis and the z-axis aligns with North pole lat=90.
"""
from math import pi

EARTH_RADIUS = 6371.

rad2deg = lambda phi: phi * (180. / pi)

deg2rad = lambda theta: theta * (pi / 180.)

def geo2sph(lat, lon, z):
    """
    Convert geographic coordinates to spherical coordinates.
    Returns r, theta, phi.
    """
    if lat < -90. or lat > 90.\
            or lon < -180. or lon > 360.\
            or z >= EARTH_RADIUS:
        raise ValueError("invalid geographic coordinates")
    theta = deg2rad(90. - lat)
    if lon < -180.:
        lon += 360.
    elif lon > 360.:
        lon -= 360.
    phi = deg2rad(lon)
    r = EARTH_RADIUS - z
    return r, theta, phi
