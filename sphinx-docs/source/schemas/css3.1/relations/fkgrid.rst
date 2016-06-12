.. _css3.1-fkgrid_relations:

**fkgrid** -- F-K grid parameters
---------------------------------

This information characterizes a single F-K grid (east-west north-south slowness grid) computed from seismic array data. The grid nodes are composed of normalized beam power values that are averaged over a time window (twin). The actual grid values can be optionally stored as external files. If nt is greater than one, then the grid is composed by stacking nt grids together.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`azimuth <css3.1-azimuth_attributes>`  |:ref:`chan <css3.1-chan_attributes>`        |:ref:`datatype <css3.1-datatype_attributes>`|:ref:`dfile <css3.1-dfile_attributes>`      |:ref:`dir <css3.1-dir_attributes>`          |:ref:`dtime <css3.1-dtime_attributes>`      |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`endtime <css3.1-endtime_attributes>`  |:ref:`filter <css3.1-filter_attributes>`    |:ref:`foff <css3.1-foff_attributes>`        |:ref:`lddate <css3.1-lddate_attributes>`    |:ref:`ne <css3.1-ne_attributes>`            |:ref:`nn <css3.1-nn_attributes>`            |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`nt <css3.1-nt_attributes>`            |:ref:`ppower <css3.1-ppower_attributes>`    |:ref:`refsta <css3.1-refsta_attributes>`    |:ref:`semax <css3.1-semax_attributes>`      |:ref:`semin <css3.1-semin_attributes>`      |:ref:`slo <css3.1-slo_attributes>`          |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`slowd <css3.1-slowd_attributes>`      |:ref:`snmax <css3.1-snmax_attributes>`      |:ref:`snmin <css3.1-snmin_attributes>`      |:ref:`sta <css3.1-sta_attributes>`          |:ref:`time <css3.1-time_attributes>`        |:ref:`twin <css3.1-twin_attributes>`        |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`                                            |:ref:`filter <css3.1-filter_attributes>`                                        |:ref:`sta <css3.1-sta_attributes>`                                              |:ref:`time <css3.1-time_attributes>`:::ref:`endtime <css3.1-endtime_attributes>`|
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

