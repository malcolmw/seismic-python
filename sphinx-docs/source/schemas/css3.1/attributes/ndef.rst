.. _css3.1-ndef_attributes:

**ndef** -- number of locating phases
-------------------------------------

This attribute is typically the number of arrivals used to
locate an event.  See timedef.  However, for catalogs from
which arrivals are not available (e.g., the PDE catalog),
ndef is filled in from the catalog, but nass is the number
of arrivals in this database which come from this event.

* **Field width:** 5
* **Format:** %5ld
* **Null:** -1
* **Range:** ndef >= 0
