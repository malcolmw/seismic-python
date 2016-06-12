.. _css3.0-instant_attributes:

**instant** -- (y,n) discrete/continuing snapshot
-------------------------------------------------

When this attribute has the value instant = 'y', it means
that the snapshot was taken at the time of a discrete
procedural change, such as an adjustment of the instrument
gain; n means the snapshot is of a continuously changing
process, such as calibration drift.  This is important for
tracking time corrections and calibrations.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** instant =~ /y|n/
