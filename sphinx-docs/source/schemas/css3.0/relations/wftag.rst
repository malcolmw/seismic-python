.. _css3.0-wftag_relations:

**wftag** -- Waveform mapping file
----------------------------------

The wftag relation links various identifiers, e.g. origin id, arrival id, stassoc id, to waveform id. All of the linkages could be determined indirectly using sta, chan and time. However, it is more efficient to predetermine them.

Fields
^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`lddate <css3.0-lddate_attributes>`  |:ref:`tagid <css3.0-tagid_attributes>`    |:ref:`tagname <css3.0-tagname_attributes>`|:ref:`wfid <css3.0-wfid_attributes>`      |
+------------------------------------------+------------------------------------------+------------------------------------------+------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------------+------------------------------------------+------------------------------------------+
|:ref:`tagid <css3.0-tagid_attributes>`    |:ref:`tagname <css3.0-tagname_attributes>`|:ref:`wfid <css3.0-wfid_attributes>`      |
+------------------------------------------+------------------------------------------+------------------------------------------+

Foreign Keys
^^^^^^^^^^^^

+------------------------------------+
|:ref:`wfid <css3.0-wfid_attributes>`|
+------------------------------------+

