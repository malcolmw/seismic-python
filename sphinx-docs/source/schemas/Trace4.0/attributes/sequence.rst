.. _Trace4.0-sequence_attributes:

**sequence** -- sequence number
-------------------------------

As a trace bundle is passed through various filters,
a history of the processing is kept in the history table.
Each trace bundle has a unique processid, and this is
the sequence number.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** sequence > 0
