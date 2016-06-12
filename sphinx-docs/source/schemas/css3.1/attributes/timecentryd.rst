.. _css3.1-timecentryd_attributes:

**timecentryd** -- epoch time of first sample in file
-----------------------------------------------------

Epoch time.  Epochal time given as seconds and fractions
of a second since hour 0 January 1, 1970, and stored in a
double precision floating number.  Refers to the relation
data object with which it is found.  E.g., in arrival -
arrival time; in origin - origin time; in wfdisc, - start
time of data.  Where date of historical events is known,
time is set to the start time of that date; where the date
of contemporary arrival measurements is known but no time
is given, then the time attribute is set to the NA value.
The double-precision floating point number allows 15
decimal digits.  At 1 millisecond accuracy this is a range
of 3 years.  Where time is unknown, or prior to Feb.  10,
1653, set to the NA value.

* **Field width:** 15
* **Format:** %15.3f
* **Null:** -9999999999.999
* **Units:** Seconds
