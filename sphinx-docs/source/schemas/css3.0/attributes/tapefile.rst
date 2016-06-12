.. _css3.0-tapefile_attributes:

**tapefile** -- tape file number
--------------------------------

This attribute gives the file number (on a tape) at which
a time-series is written.  A tape begins with file 1.
This number can be used to skip files when retrieving data
from the tape.  See tapeblock.

* **Field width:** 5
* **Format:** %5ld
* **Null:** -1
* **Range:** tapefile > 1
