.. _Trace4.0-etype_attributes:

**etype** -- event type
-----------------------

This attribute is used to identify the type of
seismic event, when known. For etypes l, r, t the value in
origin will be the value determined by the station closest
to the event.

* **Field width:** 7
* **Format:** %-7s
* **Null:** -
* **Range:** etype =~ /qb|eq|me|ex|o|l|r|t/
