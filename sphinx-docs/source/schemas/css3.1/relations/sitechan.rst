.. _css3.1-sitechan_relations:

**sitechan** -- Station-channel information
-------------------------------------------

This relation describes the orientation of a recording channel at the site referenced by sta. This relation provides information about the various channels (e.g. sz, lz, iz ) that are available at a station and maintains a record of the physical channel configuration at a site.

Fields
^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`      |:ref:`chanid <css3.1-chanid_attributes>`  |:ref:`ctype <css3.1-ctype_attributes>`    |:ref:`descrip <css3.1-descrip_attributes>`|:ref:`edepth <css3.1-edepth_attributes>`  |:ref:`hang <css3.1-hang_attributes>`      |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`lddate <css3.1-lddate_attributes>`  |:ref:`offdate <css3.1-offdate_attributes>`|:ref:`ondate <css3.1-ondate_attributes>`  |:ref:`sta <css3.1-sta_attributes>`        |:ref:`vang <css3.1-vang_attributes>`      |                                          |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+----------------------------------------+
|:ref:`chanid <css3.1-chanid_attributes>`|
+----------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`                                                |:ref:`ondate <css3.1-ondate_attributes>`:::ref:`offdate <css3.1-offdate_attributes>`|:ref:`sta <css3.1-sta_attributes>`                                                  |
+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+

Defines
^^^^^^^

+----------------------------------------+
|:ref:`chanid <css3.1-chanid_attributes>`|
+----------------------------------------+

