.. _css3.1-achanaux_relations:

**achanaux** -- map foreign chan+aux code to local chan code
------------------------------------------------------------

SEED and autoDRM use loc or aux to further specify channel, but the css3.1 schema doesn't support loc as a key. This table maps autodrm chan+aux codes to a unique local channel code, using the corresponding local sta name. Note the combination of the local sta name with the foreign chan and aux codes.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`aux <css3.1-aux_attributes>`      |:ref:`chan <css3.1-chan_attributes>`    |:ref:`fchan <css3.1-fchan_attributes>`  |:ref:`lddate <css3.1-lddate_attributes>`|:ref:`sta <css3.1-sta_attributes>`      |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------+--------------------------------------+--------------------------------------+
|:ref:`aux <css3.1-aux_attributes>`    |:ref:`fchan <css3.1-fchan_attributes>`|:ref:`sta <css3.1-sta_attributes>`    |
+--------------------------------------+--------------------------------------+--------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`chan <css3.1-chan_attributes>`|:ref:`sta <css3.1-sta_attributes>`  |
+------------------------------------+------------------------------------+

