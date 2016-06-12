.. _css3.1-magid_attributes:

**magid** -- magnitude id
-------------------------

This key is assigned to identify a network magnitude in
the netmag relation.  It is required for every network
magnitude.  Magnitudes given in origin must reference a
network magnitude with magid = mbid, mlid or msid,
whichever is appropriate.  See mbid, mlid, or msid.

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** magid > 0
