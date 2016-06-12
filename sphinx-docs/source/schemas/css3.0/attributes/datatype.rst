.. _css3.0-datatype_attributes:

**datatype** -- numeric storage
-------------------------------

this attribute specifies the format of a data series in
the file system.  the allowed datatypes are:

+-----------+-----------------------------------------------------+
|Format code|Format                                               |
+===========+=====================================================+
|aa         |alaska version of ah                                 |
+-----------+-----------------------------------------------------+
|as         |free-format ascii                                    |
+-----------+-----------------------------------------------------+
|ah         |xdr version of ah                                    |
+-----------+-----------------------------------------------------+
|ca         |canada compressed                                    |
+-----------+-----------------------------------------------------+
|c2         |ida compression of s2                                |
+-----------+-----------------------------------------------------+
|c4         |ida compression of s4                                |
+-----------+-----------------------------------------------------+
|ca         |autodrm/gse cm6 compressed ascii                     |
+-----------+-----------------------------------------------------+
|f4         |intel/dec order ieee 4 byte floats (same as u4)      |
+-----------+-----------------------------------------------------+
|g2         |gain range data                                      |
+-----------+-----------------------------------------------------+
|ic         |intel sac format                                     |
+-----------+-----------------------------------------------------+
|i2         |intel/dec order 2 byte integers                      |
+-----------+-----------------------------------------------------+
|i3         |intel/dec order 3 byte integers                      |
+-----------+-----------------------------------------------------+
|i4         |intel/dec order 4 byte integers                      |
+-----------+-----------------------------------------------------+
|ms         |mixed up miniseed: out of order, various record sizes|
+-----------+-----------------------------------------------------+
|rf         |reftek packet format                                 |
+-----------+-----------------------------------------------------+
|s2         |sparc/motorola order 2 byte integers                 |
+-----------+-----------------------------------------------------+
|s3         |sparc/motorola order 3 byte integers                 |
+-----------+-----------------------------------------------------+
|s4         |sparc/motorola order 4 byte integers                 |
+-----------+-----------------------------------------------------+
|sc         |sac format                                           |
+-----------+-----------------------------------------------------+
|sd         |steim compressed miniseed format                     |
+-----------+-----------------------------------------------------+
|s1         |steim 1 compressed miniseed format                   |
+-----------+-----------------------------------------------------+
|sy         |segy format                                          |
+-----------+-----------------------------------------------------+
|t4         |sparc/motorola order ieee 4 byte floats              |
+-----------+-----------------------------------------------------+
|u4         |intel/dec order ieee 4 byte floats                   |
+-----------+-----------------------------------------------------+
|ue         |unevenly sampled data with both time and value       |
+-----------+-----------------------------------------------------+
|zz, z      |data not saved                                       |
+-----------+-----------------------------------------------------+

note that the css standard defines many other formats,
which are not supported by the antelope software.

* **Field width:** 2
* **Format:** %-2s
* **Null:** -
* **Range:** datatype =~ /aa|as|ah|CA|c2|c4|ca|g2|i2|i3|i4|ic|rf|s2|s3|s4|sc|MS|sd|S1|sy|t4|u4|UE|zz|z/
