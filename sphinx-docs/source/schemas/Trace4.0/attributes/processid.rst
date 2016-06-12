.. _Trace4.0-processid_attributes:

**processid** -- process id
---------------------------

As a trace bundle is passed through various filters,
a history of the processing is kept in the history table.
Each trace bundle has a unique processid.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** processid > 0
