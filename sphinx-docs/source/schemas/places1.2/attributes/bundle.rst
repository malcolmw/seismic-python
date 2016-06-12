.. _places1.2-bundle_attributes:

**bundle** -- database pointer to bundled/grouped data
------------------------------------------------------

A bundle is a special database pointer which refers to
either an entire table or view, or to a contiguous subset
of some table or view.  In the former case, both the
record number and the field number should be dbALL.  In
the latter case, the record number and the field number
specify a range of records in the table.

* **Field width:** 32
* **Format:** %d %d %d %d
