.. _Trace4.0-datatype_attributes:

**datatype** -- numeric storage
-------------------------------

This attribute specifies the format of a data series in
the file system.  Datatypes t4, s4 and s2 are the allowed
values.  Datatype s4 denotes a 4-byte integer and t4
denotes a 32-bit real number in Sun format.  Machine
dependent formats are supported for common hardwares to
allow data transfer in native machine binary formats.
Note that the CSS standard defines many other formats,
which are not supported by the Antelope software.

* **Field width:** 2
* **Format:** %-2s
* **Null:** -
* **Range:** datatype =~ /t4|s4|s2/
