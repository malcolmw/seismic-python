.. _css3.1-endtime_attributes:

**endtime** -- last valid time for data
---------------------------------------

In wfdisc, this attribute is the time of the last sample
in the waveform file.  Endtime is equivalent to
time+(nsamp-1)/samprate.  In sensor, this is the last time
the data in the record are valid.

* **Field width:** 18
* **Format:** %18.6f
* **Null:** 9999999999.999000
* **Units:** Epochal seconds
* **Range:** time <= endtime
