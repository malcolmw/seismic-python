.. _Trace4.0-traces_attributes:

**traces** -- database pointer to bundled/grouped traces
--------------------------------------------------------

Abundle is a special database pointer which refers to
either an entire table or view, or to a contiguous subset
of some table or view.  In the former case, both the record
number and the field number should be dbALL.  In the latter
case, the record number and the field number specify a
range of records in the table.

* **Field width:** 32
* **Format:** %ld %ld %ld %ld
