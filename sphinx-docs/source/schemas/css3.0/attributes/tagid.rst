.. _css3.0-tagid_attributes:

**tagid** -- tagname value
--------------------------

This contains the value of a foreign key identified in
tagname.  For example, if tagname is 'arid', then wftag
may be joined to arrival where arrival.  arid = wftag.
tagid.  If tagname is 'orid', then wftag and origin may be
joined where origin.  orid = wftag.  tagid.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** tagid > 0
