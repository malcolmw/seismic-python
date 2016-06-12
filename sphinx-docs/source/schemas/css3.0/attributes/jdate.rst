.. _css3.0-jdate_attributes:

**jdate** -- julian date
------------------------

This attribute is the date of an arrival, origin, seismic
recording, etc.  The same information is available in
epoch time, but the Julian date format is more convenient
for many types of searches.  Dates B.C.  are negative.
Note: there is no year = 0000 or day = 000.  Where only
the year is known, day of year = 001; where only year and
month are known, day of year = first day of month.  Note:
only the year is negated for BC, so Jan 1 of 10 BC is
0010001.  See time.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** jdate == yearday(time)
