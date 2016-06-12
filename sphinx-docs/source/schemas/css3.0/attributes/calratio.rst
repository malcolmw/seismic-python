.. _css3.0-calratio_attributes:

**calratio** -- calibration
---------------------------

This is a dimensionless calibration correction factor
which permits small refinements to the calibration
correction made using calib and calper from the wfdisc
relation.  Often, the wfdisc calib contains the nominal
calibration assumed at the time of data recording.  If the
instrument is recalibrated, calratio provides a mechanism
to update calibrations from wfdisc with the new
information without modifying the wfdisc relation.  A
positive value means ground motion increasing in component
direction (up, north, east) is indicated by increasing
counts.  A negative value means the opposite.  Calratio is
meant to reflect the most accurate calibration information
for the time period for which the sensor record is
appropriate, but the nominal value may appear until other
information is available.

* **Field width:** 16
* **Format:** %16.6f
* **Null:** 1.000000
