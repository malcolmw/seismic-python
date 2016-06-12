.. _css3.0-syz_attributes:

**syz** -- covariance matrix element
------------------------------------

This is an element of the covariance matrix for the
location identified by orid.  The covariance matrix is
symmetric (and positive definite) so that sxy = syx, etc.,
(x,y,z,t) refer to latitude, longitude, depth and origin
time, respectively.  These attributes (together with
sdobs, ndef and dtype ) provide all the information
necessary to construct the K-dimensional (K=2,3,4)
confidence ellipse or ellipsoids at any confidence limit
desired.

* **Field width:** 15
* **Format:** %15.4f
* **Null:** -999999999.9999
* **Units:** kilometers squared,
