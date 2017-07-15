Topography
==========
A callable class providing a queryable container for surface elevation data.
Input surface elevation data must be on a regular grid. Bilinear interpolation
is used to interpolate elevation between grid points.

Constructor
------------
.. class:: seispy.topography.Topography(infile)

  :param str infile: Path to input file containing surface elevation data.

Methods
-------
.. method:: self(lat, lon)

  Return (interpolated) surface elevation at input coordinates.

  :param float lat: Latitude.
  :param float lon: Longitude.
  :return: Surface elevation at given coordinates.
  :rtype: float

Input file format
-----------------
* One data point per line.
* Three whitespace separated columns per line.

  * Column 1 - Longitude [degrees]
  * Column 2 - Latitude [degrees]
  * Column 3 - Surface elevation [meters]
