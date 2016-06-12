.. _css3.1-timeres_attributes:

**timeres** -- time residual
----------------------------

This attribute is a travel time residual, measured in
seconds.  The residual is found by taking the observed
arrival time (saved in the arrival relation) of a seismic
phase and subtracting the expected arrival time.  The
expected arrival time is calculated by a formula based on
earth velocity model (attribute vmodel ), an event
location and origin time (saved in table origin ), the
distance to the station (attribute dist in table assoc ),
and the particular seismic phase (attribute phase in table
assoc ).

* **Field width:** 8
* **Format:** %8.3f
* **Null:** -999.000
* **Units:** Seconds
