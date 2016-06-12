.. _css3.1-tapeblock_attributes:

**tapeblock** -- block number in tape file
------------------------------------------

This attribute gives the first block (in some file of an
ANSI-labeled tape) at which a time series begins.  The
dearchiving program uses this number to skip blocks within
a tape file in order to retrieve the waveform specified.
See tapefile.

* **Field width:** 5
* **Format:** %5ld
* **Null:** -1
* **Range:** tapeblock > 0
