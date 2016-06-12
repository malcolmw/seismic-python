.. _css3.1-stageid_attributes:

**stageid** -- stage number in the calibration response
-------------------------------------------------------

The ordered stage number of this discrete stage in the
calibration response.  Each individual stage corresponds
to a sensor, analog filter, A/D converter, or FIR filter.
The numbering scheme for a seismic system will generally
assign stageid=1 for the sensor, stageid=2 for the
anti-alias filter, stageid=3 for the analog-to-digital
converter, stageid=4 for the first FIR filter, ...

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** 0 < stageid
