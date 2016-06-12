.. _css3.1-isstash_attributes:

**isstash** -- (y,n) is pf object from a stash?
-----------------------------------------------

When this attribute has the value isstash = 'y', it means
that a particular parameter file object was obtained as
an ORB stash packet. Otherwise, the parameter file object
was obtained from a normal packet payload.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** isstash =~ /y|n/
