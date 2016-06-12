.. _css3.1-stage_relations:

**stage** -- filter stage calibration parameters
------------------------------------------------

Information characterizing an individual stage of the total calibration of a station-channel. Stageid provides the specific ordering in the system response for the stage. gnom, gcalib, and gunits are given for the stage. Combining all records having the same sta-chan-time will provide calib in the calibration table. This table can describe analog or digital stages. Each record provides pointers to files which contain the actual poles/zeros or digital filter coefficients.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`        |:ref:`decifac <css3.1-decifac_attributes>`  |:ref:`dfile <css3.1-dfile_attributes>`      |:ref:`dir <css3.1-dir_attributes>`          |:ref:`endtime <css3.1-endtime_attributes>`  |:ref:`gcalib <css3.1-gcalib_attributes>`    |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`gnom <css3.1-gnom_attributes>`        |:ref:`gtype <css3.1-gtype_attributes>`      |:ref:`iunits <css3.1-iunits_attributes>`    |:ref:`izero <css3.1-izero_attributes>`      |:ref:`lddate <css3.1-lddate_attributes>`    |:ref:`leadfac <css3.1-leadfac_attributes>`  |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`ounits <css3.1-ounits_attributes>`    |:ref:`samprate <css3.1-samprate_attributes>`|:ref:`ssident <css3.1-ssident_attributes>`  |:ref:`sta <css3.1-sta_attributes>`          |:ref:`stageid <css3.1-stageid_attributes>`  |:ref:`time <css3.1-time_attributes>`        |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`                                            |:ref:`sta <css3.1-sta_attributes>`                                              |:ref:`stageid <css3.1-stageid_attributes>`                                      |:ref:`time <css3.1-time_attributes>`:::ref:`endtime <css3.1-endtime_attributes>`|
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------+

