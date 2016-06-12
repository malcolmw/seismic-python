.. _Trace4.1-delta_attributes:

**delta** -- station to event distance
--------------------------------------

This attribute is the arc length of the path the seismic
phase follows from source to receiver. The location of the
origin is specified in the origin record referenced by the
attribute orid. The attribute arid points to the record in
the arrival relation that identifies the receiver. The
value of the attribute can exceed 180 degrees, it can even
exceed 360 degrees. The geographic distance between source
and receiver is delta mod(180).

* **Field width:** 8
* **Format:** %8.3f
* **Null:** -1.000
* **Units:** Degrees
* **Range:** delta >= 0.0
