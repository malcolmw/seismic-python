FaultCollection
===============
A containter class providing convenience functions to read and subset fault
trace data.

Constructor
-----------
.. class:: seispy.faults.FaultCollection(infile)

  :param str infile: Path to input file containing fault surface trace data.

Instance attributes
~~~~~~~~~~~~~~~~~~~
.. attribute:: data

  numpy.ndarray of fault surface trace segments. Each segment is a ndarray
  of geographic coordinates (eg. array([[33, -115], [33.1, -115.2], ...])).

Public Methods
--------------
.. method:: subset(latmin, latmax, lonmin, lonmax)

  :param float latmin: Minimum latitude of bounding box.
  :param float latmax: Maximum latitude of bounding box.
  :param float lonmin: Minimum longitude of bounding box.
  :param float lonmax: Maximum longitude of bounding box.
  :returns: Array of fault trace segments.
  :rtype: numpy.ndarray
