.. _css3.1-clip_attributes:

**clip** -- clipped flag
------------------------

This is a single-character flag to indicate whether (c) or
not (n) the data were clipped.  Typically, this flag is
derived from status bits supplied with GDSN or RSTN data,
but could also be supplied as a result of analyst review.

For some data, a 'T' or a 't' in this field indicates
a time correction was applied.  The exact correction
should be found in the associated wfdisc_tshift table.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** clip =~ /c|n|T|t/
