.. _css3.0-wfmeas_relations:

**wfmeas** -- waveform measurements
-----------------------------------

This relation provides a general way to store measurements made on segments of waveform data. The time::endtime fields give the time window of the data for which the measurement is unique. tmeas and twin specify the beginning of the measurement time for discrete measurements, and the time-span for extended measurements. The contents of val1 and val2, described by units1 and units2, depend on the type of measurement made.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`arid <css3.0-arid_attributes>`        |:ref:`auth <css3.0-auth_attributes>`        |:ref:`chan <css3.0-chan_attributes>`        |:ref:`endtime <css3.0-endtime_attributes>`  |:ref:`filter <css3.0-filter_attributes>`    |:ref:`lddate <css3.0-lddate_attributes>`    |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`meastype <css3.0-meastype_attributes>`|:ref:`sta <css3.0-sta_attributes>`          |:ref:`time <css3.0-time_attributes>`        |:ref:`tmeas <css3.0-tmeas_attributes>`      |:ref:`twin <css3.0-twin_attributes>`        |:ref:`units1 <css3.0-units1_attributes>`    |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`units2 <css3.0-units2_attributes>`    |:ref:`val1 <css3.0-val1_attributes>`        |:ref:`val2 <css3.0-val2_attributes>`        |                                            |                                            |                                            |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`        |:ref:`endtime <css3.0-endtime_attributes>`  |:ref:`filter <css3.0-filter_attributes>`    |:ref:`meastype <css3.0-meastype_attributes>`|:ref:`sta <css3.0-sta_attributes>`          |:ref:`time <css3.0-time_attributes>`        |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Foreign Keys
^^^^^^^^^^^^

+------------------------------------+
|:ref:`arid <css3.0-arid_attributes>`|
+------------------------------------+

