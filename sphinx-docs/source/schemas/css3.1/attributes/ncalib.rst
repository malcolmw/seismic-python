.. _css3.1-ncalib_attributes:

**ncalib** -- nominal calibration
---------------------------------

This is the conversion factor that maps digital data to
earth displacement.  The factor holds true at the
oscillation period specified by ncalper.  A positive value
means ground motion increasing in component direction (up,
north, east) is indicated by increasing counts.  A
negative value means the opposite.  Actual calibration for
a particular recording is determined using the wfdisc and
sensor relations.  See calratio.

* **Field width:** 16
* **Format:** %16.6f
* **Null:** -99.999999
* **Units:** Nanometers/digital count
