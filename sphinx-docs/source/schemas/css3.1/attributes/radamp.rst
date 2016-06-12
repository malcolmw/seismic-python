.. _css3.1-radamp_attributes:

**radamp** -- Radiation pattern predicted amplitude
---------------------------------------------------

A source has a body wave radiation pattern whose predicted
magnitude is to be stored in this field.  Because it is
a radiation pattern effect it should be scaled from 0 to 1.
This is useful for conventional focal mechanism, but less
useful for moment tensor solutions.

* **Field width:** 10
* **Format:** %10.7f
* **Null:** -1.0000000
* **Units:** nondimensional
* **Range:** 1.0 >= amp >= 0.0
