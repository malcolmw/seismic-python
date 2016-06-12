.. _css3.0-fkgrid_relations:

**fkgrid** -- F-K grid parameters
---------------------------------

This information characterizes a single F-K grid (east-west north-south slowness grid) computed from seismic array data. The grid nodes are composed of normalized beam power values that are averaged over a time window (twin). The actual grid values can be optionally stored as external files. If nt is greater than one, then the grid is composed by stacking nt grids together.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`azimuth <css3.0-azimuth_attributes>`  |:ref:`chan <css3.0-chan_attributes>`        |:ref:`datatype <css3.0-datatype_attributes>`|:ref:`dfile <css3.0-dfile_attributes>`      |:ref:`dir <css3.0-dir_attributes>`          |:ref:`dtime <css3.0-dtime_attributes>`      |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`endtime <css3.0-endtime_attributes>`  |:ref:`filter <css3.0-filter_attributes>`    |:ref:`foff <css3.0-foff_attributes>`        |:ref:`lddate <css3.0-lddate_attributes>`    |:ref:`ne <css3.0-ne_attributes>`            |:ref:`nn <css3.0-nn_attributes>`            |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`nt <css3.0-nt_attributes>`            |:ref:`ppower <css3.0-ppower_attributes>`    |:ref:`refsta <css3.0-refsta_attributes>`    |:ref:`semax <css3.0-semax_attributes>`      |:ref:`semin <css3.0-semin_attributes>`      |:ref:`slo <css3.0-slo_attributes>`          |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`slowd <css3.0-slowd_attributes>`      |:ref:`snmax <css3.0-snmax_attributes>`      |:ref:`snmin <css3.0-snmin_attributes>`      |:ref:`sta <css3.0-sta_attributes>`          |:ref:`time <css3.0-time_attributes>`        |:ref:`twin <css3.0-twin_attributes>`        |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`                                            |:ref:`filter <css3.0-filter_attributes>`                                        |:ref:`sta <css3.0-sta_attributes>`                                              |:ref:`time <css3.0-time_attributes>`:::ref:`endtime <css3.0-endtime_attributes>`|
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

