.. _css3.0-rayleigh_attributes:

**rayleigh** -- Rayleigh bin size in cycles/sec
-----------------------------------------------

This parameter is relevant for multitaper spectra which have
well defined properties in terms of the time-bandwidth
product and this parameter.  The rayleigh bin size
differs from the number of delta frequency when zero
padding is used or when the time series are tapered.
Rayleigh bins are determined by the
of actual length of the time series and the time-bandwidth
product of the taper while the number of
frequency interval size is
dependent upon the amount of zero padding used.

* **Field width:** 15
* **Format:** %15.6lg
* **Null:** -1
* **Units:** Hertz
* **Range:** rayleigh > 0.0
