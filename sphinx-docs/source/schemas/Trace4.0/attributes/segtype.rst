.. _Trace4.0-segtype_attributes:

**segtype** -- indexing method
------------------------------

Originally, this attribute indicated if a waveform were
o(original), v(virtual), s(segmented) or d(duplicate).
However, in Antelope datasets, it indicates the "natural"
units of the detector -- 'A' (acceleration), 'V' (velocity),
or 'D' (displacement).

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** segtype =~ /A|V|D/
