.. _css3.0-qual_attributes:

**qual** -- signal onset quality
--------------------------------

This single-character flag is used to denote the sharpness
of the onset of a seismic phase.  This relates to the
timing accuracy as follows: i (impulsive) - accurate to +/
0.2 seconds e (emergent) - accuracy between +/ (0.2 to 1.0
seconds) w (weak) - timing uncertain to > 1 second.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** qual =~ /i|e|w/
