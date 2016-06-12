.. _css3.0-stassid_attributes:

**stassid** -- stassoc id
-------------------------

The wavetrain from a single event may be made up of a
number of arrivals.  A unique stassid joins those arrivals
believed to have come from a common event as measured at a
single station.  Stassid is also the key to the stassoc
relation, which contains additional signal measurements
not contained within the arrival relation, such as station
magnitude estimates and computed signal characteristics.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** stassid > 0
