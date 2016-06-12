.. _css3.1-arid_attributes:

**arid** -- arrival id
----------------------

Each arrival is assigned a unique positive integer
identifying it with a unique sta, chan and time.  This
number is used in the assoc relation along with the origin
identifier to link arrival and origin.

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** arid > 0
