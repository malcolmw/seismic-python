.. _css3.0-freqmin_attributes:

**freqmin** -- Frequency of first point in spectral file
--------------------------------------------------------

Most spectra have zero as the first frequency, but we
need to add this field to allow possibility of starting
at a nonzero value.

* **Field width:** 15
* **Format:** %15.6lg
* **Null:** -1
* **Units:** Hertz
* **Range:** freqmin >= 0.0
