.. _css3.0-commid_attributes:

**commid** -- comment id
------------------------

This is a key used to point to free-form comments entered
in the remark relation.  These comments store additional
information about a tuple in another relation.  Within the
remark relation, there may be many tuples with the same
commid and different lineno, but the same commid will
appear in only one other tuple among the rest of the
relations in the database.  See lineno.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** commid > 0
