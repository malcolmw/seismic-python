.. _css3.1-etype_attributes:

**etype** -- event type
-----------------------

This attribute is used to identify the type of seismic
event, when known.  For etypes l, r, t the value in origin
will be the value determined by the station closest to the
event.  Event with etype set to f were felt.

* **Field width:** 2
* **Format:** %-2s
* **Null:** -
* **Range:** etype =~ /qb|eq|me|ex|o|l|r|t|f/
