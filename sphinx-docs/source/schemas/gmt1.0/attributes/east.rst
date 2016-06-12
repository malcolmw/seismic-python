.. _gmt1.0-east_attributes:

**east** -- easternmost longitude of file
-----------------------------------------

This field records the eastern longitude boundary of the
GMT file. The phase may be unwrapped, in which case
longitudes of -180 to 0 may appear as 180 to 360 degrees.

* **Field width:** 9
* **Format:** %9.4lf
* **Null:** -999.0000
* **Units:** Degrees
* **Range:** east >= -180 && east <= 360
