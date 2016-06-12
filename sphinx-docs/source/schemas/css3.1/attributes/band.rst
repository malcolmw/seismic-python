.. _css3.1-band_attributes:

**band** -- frequency band
--------------------------

This is a qualitative indicator of frequency pass-band for
an instrument.  Values should reflect the response curve
rather than just the sample rate.  Recommended values are
s (short-period), m (mid-period), i (intermediate-period),
l (long-period), b (broad-band), h (high frequency, very
short-period), and v (very long-period).  For a better
notion of the instrument characteristics, see the
instrument response curve.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** band =~ /s|m|i|l|b|h|v/
