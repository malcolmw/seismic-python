.. _css3.0-site_relations:

**site** -- Station location information
----------------------------------------

Site names and describes a point on the earth where seismic measurements are made ( e.g. the location of a seismic instrument or array). It contains information that normally changes infrequently, such as location. In addition, site contains fields to describe the offset of a station relative to an array reference location. Global data integrity implies that the sta/ondate in site be consistent with the sta/chan/ondate in sitechan.

Fields
^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`deast <css3.0-deast_attributes>`    |:ref:`dnorth <css3.0-dnorth_attributes>`  |:ref:`elev <css3.0-elev_attributes>`      |:ref:`lat <css3.0-lat_attributes>`        |:ref:`lddate <css3.0-lddate_attributes>`  |:ref:`lon <css3.0-lon_attributes>`        |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`offdate <css3.0-offdate_attributes>`|:ref:`ondate <css3.0-ondate_attributes>`  |:ref:`refsta <css3.0-refsta_attributes>`  |:ref:`sta <css3.0-sta_attributes>`        |:ref:`staname <css3.0-staname_attributes>`|:ref:`statype <css3.0-statype_attributes>`|
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|:ref:`ondate <css3.0-ondate_attributes>`:::ref:`offdate <css3.0-offdate_attributes>`|:ref:`sta <css3.0-sta_attributes>`                                                  |
+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+

