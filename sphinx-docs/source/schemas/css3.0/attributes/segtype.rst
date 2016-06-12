.. _css3.0-segtype_attributes:

**segtype** -- detector measurement type / natural units
--------------------------------------------------------

Originally, this attribute indicated if a waveform were
o(original), v(virtual), s(segmented) or d(duplicate).
However, in Antelope datasets, it indicates the "natural"
units of the detector -- 'A' (acceleration), 'V'
(velocity), 'D' (displacement), 'I' (infrasound), or 'H'
(hydroacoustic), and more recently a host of other non-seismic
measurements.

+--------+-----------------+---------------------------------+
|segtype | units           |type of data                     |
+========+=================+=================================+
| A      | nm/sec/sec      |acceleration                     |
+--------+-----------------+---------------------------------+
| B      | 25*mw/m/m       |UV (sunburn) index (NOAA)        |
+--------+-----------------+---------------------------------+
| D      | nm              |displacement                     |
+--------+-----------------+---------------------------------+
| H      | pascal          |hydroacoustic                    |
+--------+-----------------+---------------------------------+
| I      | pascal          |infrasound                       |
+--------+-----------------+---------------------------------+
| J      | watts           |power (Joules/sec) (UCSD)        |
+--------+-----------------+---------------------------------+
| K      | kilopascal      |generic pressure (UCSB)          |
+--------+-----------------+---------------------------------+
| M      | millimeters     |Wood-Anderson drum recorder      |
+--------+-----------------+---------------------------------+
| N      | -               |dimensionless                    |
+--------+-----------------+---------------------------------+
| P      | millibar        |barometric pressure              |
+--------+-----------------+---------------------------------+
| R      | millimeters     |rain fall (UCSD)                 |
+--------+-----------------+---------------------------------+
| S      | nm/m            |strain                           |
+--------+-----------------+---------------------------------+
| T      | seconds         |time                             |
+--------+-----------------+---------------------------------+
| V      | nm/sec          |velocity                         |
+--------+-----------------+---------------------------------+
| W      | watts/m/m       |insolation                       |
+--------+-----------------+---------------------------------+
| X      | nm*sec          |integrated displacement          |
+--------+-----------------+---------------------------------+
| Y      | power           |waveform power                   |
+--------+-----------------+---------------------------------+
| a      | degrees         |azimuth                          |
+--------+-----------------+---------------------------------+
| b      | bits/second     |bit rate                         |
+--------+-----------------+---------------------------------+
| c      | counts          |dimensionless integer            |
+--------+-----------------+---------------------------------+
| d      | meters          |depth or height (e.g., water)    |
+--------+-----------------+---------------------------------+
| f      | micromoles/s/m/m|photoactive radiation flux       |
+--------+-----------------+---------------------------------+
| h      | pH              |hydrogen ion concentration       |
+--------+-----------------+---------------------------------+
| i      | amperes         |electric current                 |
+--------+-----------------+---------------------------------+
| j      | counts/m/m/s    |hail intensity                   |
+--------+-----------------+---------------------------------+
| l      | sec/km          |slowness                         |
+--------+-----------------+---------------------------------+
| m      | bitmap          |dimensionless bitmap             |
+--------+-----------------+---------------------------------+
| n      | nanoradians     |angle (tilt)                     |
+--------+-----------------+---------------------------------+
| o      | milligrams/liter|dilution of oxygen (Mark VanScoy)|
+--------+-----------------+---------------------------------+
| p      | percent         |percentage                       |
+--------+-----------------+---------------------------------+
| r      | inches          |rainfall (UCSD)                  |
+--------+-----------------+---------------------------------+
| s      | meter/second    |speed (e.g., wind)               |
+--------+-----------------+---------------------------------+
| t      | degrees_Celsius |temperature                      |
+--------+-----------------+---------------------------------+
| u      | microsiemens/cm |conductivity                     |
+--------+-----------------+---------------------------------+
| v      | volts           |electric potential               |
+--------+-----------------+---------------------------------+
| w      | radians/second  |rotation rate                    |
+--------+-----------------+---------------------------------+

* **Field width:** 1
* **Format:** %-1s
* **Null:** -
* **Range:** segtype =~ /A|B|D|H|I|J|M|N|P|R|S|T|V|W|X|Y|a|b|c|d|f|h|i|j|l|m|n|o|p|r|s|t|u|v|x/
