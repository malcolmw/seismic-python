.. _places1.2-regions_relations:

**regions** -- Vertices defining regions of interest
----------------------------------------------------

This table specifies the vertex locations for the polygons enclosing each region. The vertex field indicates the ordering of the vertices around the polygon. For implementations which need to distinguish unambiguously the difference between the inside and outside of a region, usually for regions that include significant fractions of the globe or regions that might be on the far side of the globe from a possibly included earthquake, the vertices should be listed in clockwise order looking down at the surface in map view. For situations in which there may be several types of overlapping regions, or overlapping regions which need to be ranked in priority, additional tables should be defined in an expansion schema.

Fields
^^^^^^

+---------------------------------------------+---------------------------------------------+---------------------------------------------+---------------------------------------------+
|:ref:`lat <places1.2-lat_attributes>`        |:ref:`lon <places1.2-lon_attributes>`        |:ref:`regname <places1.2-regname_attributes>`|:ref:`vertex <places1.2-vertex_attributes>`  |
+---------------------------------------------+---------------------------------------------+---------------------------------------------+---------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+---------------------------------------------+---------------------------------------------+
|:ref:`regname <places1.2-regname_attributes>`|:ref:`vertex <places1.2-vertex_attributes>`  |
+---------------------------------------------+---------------------------------------------+

