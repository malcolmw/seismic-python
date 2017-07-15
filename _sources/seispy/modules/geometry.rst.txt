geometry
========

.. automodule:: seispy.geometry
  :members:

Coordinate systems
------------------
For all coordinate systems, the coordinate system origin is at the center of the
Earth.

Geographic
~~~~~~~~~~
The geographic coordinate system describes the position of a point relative to
the center of the Earth with latitude, longitude and depth coordinates.

* Latitude - The latitude above/below the equator.

  * Abbreviation: lat
  * Units: degrees
  * Range: [-90, 90]

* Longitude - The longitude East/West of the Prime Meridian.

  * Abbreviation: lon
  * Units: degrees
  * Range: [-180, 360]

* Depth - The depth below the *(idealized)* surface of the Earth. Use a negative
  depth for points above the surface.

  * Units: km
  * Range: (-inf, seispy.constants.EARTH_RADIUS]

Spherical
~~~~~~~~~
The spherical coordinate system describes the position of a point relative to
the center of the Earth with radial distance, polar angle and azimuthal angle
coordinates. The polar angle is measured relative to the geographic North pole
(i.e. lat=90) and the azimuthal angle is measure relative to the geographic
Prime Meridian (i.e. lon=0).

* Radial coordinate - The radial distance from the center of the Earth.

  * Abbreviation: r
  * Units: km
  * Range: [0, inf)

* Polar coordinate - The angle subtended by a line connecting the center of the
  Earth to the North pole and a line connecting the coordinate system origin to
  the point described.

  * Abbreviation: theta, θ
  * Units: Radians
  * Range: [0, π]

* Azimuthal coordinate - The angle subtended by a line connecting the coordinate
  system origin to the intersection of the Prime Meridian and Equator and the line
  connecting the origin with the point being described.

  * Abbreviation: phi, φ
  * Units: Radians
  * Range: [0, 2π]

Cartesian
~~~~~~~~~
The cartesian coordinate system describes the position of a point relative
to the center of the Earth with familiar (x, y, z) coordinates.

* The x-axis pierces the intersection of the Prime Meridian and Equator
  (point (0, 0, 0) in geographic coordinates).
* The y-axis pierces the the point with geographic coordinates (0, 90, 0).
* The z-axis pierces the North pole (point (90, 0, 0) in geographic coordinates).
