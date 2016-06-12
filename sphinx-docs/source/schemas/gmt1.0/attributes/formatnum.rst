.. _gmt1.0-formatnum_attributes:

**formatnum** -- grdfile format number
--------------------------------------

The formatnum field records the GMT format-number
type of the grid file. Predefined format numbers are:

0. GMT netCDF 4-byte float format [Default]
1. Native binary single precision floats in scanlines
with leading grd header
2. Native binary short integers in scanlines with leading
grd header
3. 8-bit standard Sun rasterfile (colormap ignored)
4. Native binary unsigned char in scanlines with leading
grd header
5. Native binary bits in scanlines with leading grd header
6. Native binary ``surfer'' grid files
7. netCDF 1-byte byte format
8. netCDF 1-byte char format
9. netCDF 2-byte int format
10. netCDF 4-byte int format
11. netCDF 8-byte double format

* **Field width:** 10
* **Format:** %10d
* **Null:** -1
* **Range:** formatnum >= 0
