.. _css3.0-spectype_attributes:

**spectype** -- Spectrum file type
----------------------------------

This attribute describes the type of estimate the file
associated with this relation points to.  Valid types
anticipated at this revision include:
sp1c     - power spectrum estimate from single component
sp3c     - total power estimate from 3 components
asp1c    - amplitude spectrum estimate from single component
asp3c    - total amplitude estimate from 3 components
clow     - lower confidence limit
chi      - upper confidence limit
low      - lower bound of ensemble of spectral estimates
high     - upper bound of ensemble of spectral estimates
1_4      - lower quartile of ensemble
3_4      - upper quartile of ensemble
response - response spectrum estimate from single component

* **Field width:** 8
* **Format:** %-8s
