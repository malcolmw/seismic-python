.. _css3.1-samprate_attributes:

**samprate** -- sampling rate in samples/sec
--------------------------------------------

This attribute is the sample rate in samples/second.  In
the instrument relation this is specifically the nominal
sample rate, not accounting for clock drift.  In wfdisc,
the value may vary slightly from the nominal to reflect
clock drift.

Some special channels, like log channels, have this set to zero.

* **Field width:** 14
* **Format:** %14.7f
* **Null:** -1.0000000
* **Units:** 1/seconds
* **Range:** samprate >= 0.0
