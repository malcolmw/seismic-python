.. _css3.1-statype_attributes:

**statype** -- station type: single station, virt. array, etc.
--------------------------------------------------------------

This character string specifies the station type.
Recommended entries are ss (single station) or ar (array).
For autodrm, the only allowed values are
1C = single component
3C = three component
hfa = high-frequency array
lpa = long period array

* **Field width:** 4
* **Format:** %-4s
* **Null:** -
* **Range:** statype =~ /ss|ar|1C|3C|hfa|lpa/
