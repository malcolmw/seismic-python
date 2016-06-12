.. _Trace4.0-dbptr_attributes:

**dbptr** -- original database pointer
--------------------------------------

Often, actual waveform data will have arisen
from a single row in an input database table.  This
database pointer references that row.  The information
in the tables which this pointer references may not
apply to the current trace, however.

* **Field width:** 32
* **Format:** %ld %ld %ld %ld
* **Null:** -102 -102 -102 -102
