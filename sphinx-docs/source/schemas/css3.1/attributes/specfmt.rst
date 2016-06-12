.. _css3.1-specfmt_attributes:

**specfmt** -- Format of spectra file
-------------------------------------

This attribute describes the format of the spectra file.
The intent is to have two allowable values:
fap2 - which are the ascii files used by the response library
this format allows for representations of spectra with
non-constant df.
binary - assumes that the spectra file is stored as real numbers
This format may be useful when calculating huge numbers
of spectra.  No specific I/O routines exist for this yet.

fap2 format is the only one implemented at present.

* **Field width:** 12
* **Format:** %-12s
* **Null:** -
* **Range:** specfmt =~ /fap2/
