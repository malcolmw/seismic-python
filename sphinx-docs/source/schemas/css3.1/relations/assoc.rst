.. _css3.1-assoc_relations:

**assoc** -- Data associating arrivals with origins
---------------------------------------------------

This table has information that connects arrivals (i.e., entries in the arrival relation) to a particular origin. It has a composite key made of arid and orid. There are two kinds of measurement data: three attributes are related to the station ( delta, seaz, esaz ), and the remaining measurement attributes are jointly determined by the measurements made on the seismic wave ( arrival ), and the inferred event's origin ( origin ). The attribute sta is intentionally duplicated in this table to eliminate the need for a join with arrival when doing a lookup on station.

Fields
^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`      |:ref:`azdef <css3.1-azdef_attributes>`    |:ref:`azres <css3.1-azres_attributes>`    |:ref:`belief <css3.1-belief_attributes>`  |:ref:`commid <css3.1-commid_attributes>`  |:ref:`delta <css3.1-delta_attributes>`    |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`emares <css3.1-emares_attributes>`  |:ref:`esaz <css3.1-esaz_attributes>`      |:ref:`lddate <css3.1-lddate_attributes>`  |:ref:`orid <css3.1-orid_attributes>`      |:ref:`phase <css3.1-phase_attributes>`    |:ref:`seaz <css3.1-seaz_attributes>`      |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`slodef <css3.1-slodef_attributes>`  |:ref:`slores <css3.1-slores_attributes>`  |:ref:`sta <css3.1-sta_attributes>`        |:ref:`timedef <css3.1-timedef_attributes>`|:ref:`timeres <css3.1-timeres_attributes>`|:ref:`vmodel <css3.1-vmodel_attributes>`  |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`wgt <css3.1-wgt_attributes>`        |                                          |                                          |                                          |                                          |                                          |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`|:ref:`orid <css3.1-orid_attributes>`|
+------------------------------------+------------------------------------+

Foreign Keys
^^^^^^^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`    |:ref:`commid <css3.1-commid_attributes>`|:ref:`orid <css3.1-orid_attributes>`    |
+----------------------------------------+----------------------------------------+----------------------------------------+

