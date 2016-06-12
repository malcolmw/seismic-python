.. _css3.0-calib_attributes:

**calib** -- nominal calibration
--------------------------------

This is the conversion factor that maps digital seismic data to
displacement, velocity, or acceleration, depending on the
value of segtype or rsptype.  The factor holds true at the
oscillation period specified by the attribute calper.  A
positive value means ground motion (velocity,
acceleration) increasing in the component direction (up,
north, east) is indicated by increasing counts.  A
negative value means the opposite.  Calib generally
reflects the best calibration information available at the
time of recording, but refinement may be given in sensor
reflecting a subsequent recalibration of the instrument.
See calratio.

* **Field width:** 16
* **Format:** %16.9g
* **Null:** 0
* **Units:** Nanometers/digital count
* **Range:** calib > 0.0
