.. _css3.0-dtype_attributes:

**dtype** -- depth method used
------------------------------

This single-character flag indicates the method by which
the depth was determined or constrained during the
location process.  The recommended values are f (free), d
(from depth phases), r (restrained by location program) or
g (restrained by geophysicist).  In cases r or g, either
the auth field should indicate the agency or person
responsible for this action, or the commid field should
point to an explanation in the remark relation.

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** dtype =~ /f|d|r|g/
