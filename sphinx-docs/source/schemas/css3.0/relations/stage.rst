.. _css3.0-stage_relations:

**stage** -- filter stage calibration parameters
------------------------------------------------

Information characterizing an individual stage of the total calibration of a station-channel. Stageid provides the specific ordering in the system response for the stage. gnom, gcalib, and gunits are given for the stage. Combining all records having the same sta-chan-time will provide calib in the calibration table. This table can describe analog or digital stages. Each record provides pointers to files which contain the actual poles/zeros or digital filter coefficients.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`        |:ref:`decifac <css3.0-decifac_attributes>`  |:ref:`dfile <css3.0-dfile_attributes>`      |:ref:`dir <css3.0-dir_attributes>`          |:ref:`endtime <css3.0-endtime_attributes>`  |:ref:`gcalib <css3.0-gcalib_attributes>`    |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`gnom <css3.0-gnom_attributes>`        |:ref:`gtype <css3.0-gtype_attributes>`      |:ref:`iunits <css3.0-iunits_attributes>`    |:ref:`izero <css3.0-izero_attributes>`      |:ref:`lddate <css3.0-lddate_attributes>`    |:ref:`leadfac <css3.0-leadfac_attributes>`  |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`ounits <css3.0-ounits_attributes>`    |:ref:`samprate <css3.0-samprate_attributes>`|:ref:`ssident <css3.0-ssident_attributes>`  |:ref:`sta <css3.0-sta_attributes>`          |:ref:`stageid <css3.0-stageid_attributes>`  |:ref:`time <css3.0-time_attributes>`        |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`                                            |:ref:`sta <css3.0-sta_attributes>`                                              |:ref:`stageid <css3.0-stageid_attributes>`                                      |:ref:`time <css3.0-time_attributes>`:::ref:`endtime <css3.0-endtime_attributes>`|
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

