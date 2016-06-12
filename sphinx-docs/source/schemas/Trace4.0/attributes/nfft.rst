.. _Trace4.0-nfft_attributes:

**nfft** -- number of points to use in the fft
----------------------------------------------

This is the size of array on which the fft is
calculated.  This is typically around 2*nsamp+1
(the second half of the array is zero filled),
in order to increase the resolution in the frequency
domain.

* **Field width:** 8
* **Format:** %8ld
* **Null:** 0
* **Range:** nfft > 0
