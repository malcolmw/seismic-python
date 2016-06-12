.. _css3.0-leadfac_attributes:

**leadfac** -- leading factor
-----------------------------

This factor is used to correct the situation of using a
24-bit A/D converter and storing the data in a 4 byte
word.  If the data are stored in the lower 3 bytes of the
4 byte word then leadfac=1.0 If the data are stored in the
high bytes then it will be a large factor which is divided
from gnom.

* **Field width:** 11
* **Format:** %11.7f
* **Null:** 0.0000000
* **Range:** leadfac > 0.0
