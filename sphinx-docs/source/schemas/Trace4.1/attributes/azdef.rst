.. _Trace4.1-azdef_attributes:

**azdef** -- azimuth = defining, non-defining
---------------------------------------------

This is a one character flag that
indicates whether or not the azimuth of a phase was used to
determine the event's origin. It is defining (azdef=d)
if used to help locate the event or non-defining (azdef=n)
if it is not used.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** azdef =~ /d|n/
