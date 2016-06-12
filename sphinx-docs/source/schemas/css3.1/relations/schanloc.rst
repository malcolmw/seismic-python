.. _css3.1-schanloc_relations:

**schanloc** -- map foreign chan+loc code to local chan code
------------------------------------------------------------

SEED and autoDRM use loc or aux to further specify channel, but the css3.1 schema doesn't support loc as a key. This table maps seed chan+loc codes to a unique local channel code, using the corresponding local sta name. Note the combination of the local sta name with the foreign chan and loc codes.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`    |:ref:`fchan <css3.1-fchan_attributes>`  |:ref:`lddate <css3.1-lddate_attributes>`|:ref:`loc <css3.1-loc_attributes>`      |:ref:`sta <css3.1-sta_attributes>`      |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`|:ref:`sta <css3.1-sta_attributes>`  |
+------------------------------------+------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+--------------------------------------+--------------------------------------+--------------------------------------+
|:ref:`fchan <css3.1-fchan_attributes>`|:ref:`loc <css3.1-loc_attributes>`    |:ref:`sta <css3.1-sta_attributes>`    |
+--------------------------------------+--------------------------------------+--------------------------------------+

