.. _css3.1-mechid_attributes:

**mechid** -- mechanism id
--------------------------

Each focal mechanism needs to assigned a unique mechanism
id.  A seperate key from orid is necessary because it is
possible for different methods to be used to produce different
solutions from the same first motion data.  Note this
key is for traditional focal mechanism solutions only.
The moment table is used for moment tensor solutions and
each moment tensor solution will have a unique orid.

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** mechid > 0
