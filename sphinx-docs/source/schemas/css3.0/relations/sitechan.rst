.. _css3.0-sitechan_relations:

**sitechan** -- Station-channel information
-------------------------------------------

This relation describes the orientation of a recording channel at the site referenced by sta. This relation provides information about the various channels (e.g. sz, lz, iz ) that are available at a station and maintains a record of the physical channel configuration at a site.

Fields
^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`      |:ref:`chanid <css3.0-chanid_attributes>`  |:ref:`ctype <css3.0-ctype_attributes>`    |:ref:`descrip <css3.0-descrip_attributes>`|:ref:`edepth <css3.0-edepth_attributes>`  |:ref:`hang <css3.0-hang_attributes>`      |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`lddate <css3.0-lddate_attributes>`  |:ref:`offdate <css3.0-offdate_attributes>`|:ref:`ondate <css3.0-ondate_attributes>`  |:ref:`sta <css3.0-sta_attributes>`        |:ref:`vang <css3.0-vang_attributes>`      |                                          |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+----------------------------------------+
|:ref:`chanid <css3.0-chanid_attributes>`|
+----------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|:ref:`chan <css3.0-chan_attributes>`                                                |:ref:`ondate <css3.0-ondate_attributes>`:::ref:`offdate <css3.0-offdate_attributes>`|:ref:`sta <css3.0-sta_attributes>`                                                  |
+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+

Defines
^^^^^^^

+----------------------------------------+
|:ref:`chanid <css3.0-chanid_attributes>`|
+----------------------------------------+

