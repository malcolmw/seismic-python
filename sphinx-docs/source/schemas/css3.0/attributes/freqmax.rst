.. _css3.0-freqmax_attributes:

**freqmax** -- Frequency of last point in spectral file
-------------------------------------------------------

Most spectra have the Nyquist frequency as the last frequency, but we
need to add this field to allow possibility of starting
at a nonzero value.

* **Field width:** 15
* **Format:** %15.6lg
* **Null:** -1
* **Units:** Hertz
* **Range:** freqmax >= freqmin
