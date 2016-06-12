.. _css3.1-keyvalue_attributes:

**keyvalue** -- last value used for that id
-------------------------------------------

This attribute maintains the last assigned value (a
positive integer) of the counter for the specified
keyname.  The number keyvalue is the last counter value
used for the attribute keyname.  Key values are maintained
in the database to ensure uniqueness.

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** keyvalue > 0 && keyvalue < 999999998999
