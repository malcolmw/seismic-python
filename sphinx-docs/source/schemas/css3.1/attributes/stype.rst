.. _css3.1-stype_attributes:

**stype** -- signal type
------------------------

This single-character flag indicates the event or signal
type.  The following event types are defined: l (local), r
(regional), t (teleseismic), m (mixed or multiple), g
(glitch), c (calibration activity upsets the date).  l, r,
and t are supplied by the reporting station, or as an
output of post detection processing.  g and c come from
analyst comment or from the status bits from GDSN and RSTN
data.  stype is also used in the wfrms table to indicate
signal (s) or noise (n)

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** stype =~ /l|r|t|m|g|c|s|n|1|2|3/
