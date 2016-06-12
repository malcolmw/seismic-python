.. _css3.1-ondate_attributes:

**ondate** -- Julian start date
-------------------------------

This attribute is the Julian Date on which the station or
sensor indicated began operating.  Offdate and ondate are
not intended to accommodate temporary downtimes, but
rather to indicate the time period for which the
attributes of the station ( lat, lon, elev ) are valid for
the given station code.  Stations are often moved, but
with the station code remaining unchanged.

* **Field width:** 18
* **Format:** %18ld
* **Null:** -1
* **Range:** ondate >= 1900001&& ondate <= 2100000
