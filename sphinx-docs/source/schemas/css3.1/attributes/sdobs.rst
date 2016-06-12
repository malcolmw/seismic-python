.. _css3.1-sdobs_attributes:

**sdobs** -- standard error of observation
------------------------------------------

This attribute is derived from the discrepancies in the
arrival times of the phases used to locate an event.  It
is defined as the square root of the sum of the squares of
the time residuals, divided by the number of degrees of
freedom.  The latter is the number of defining
observations (ndef in origin) minus the dimension of the
system solved (4 if depth is allowed to be a free
variable, 3 if depth is constrained).

* **Field width:** 9
* **Format:** %9.4f
* **Null:** -1.0000
* **Range:** sdobs > 0.0
