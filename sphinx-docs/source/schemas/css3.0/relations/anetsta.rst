.. _css3.0-anetsta_relations:

**anetsta** -- map autodrm net+sta code to local sta code
---------------------------------------------------------

SEED and autoDRM use network to further specify station, but the css3.0 schema doesn't support net as a key whereever sta is used. This table maps foreign autodrm net+sta codes to a unique local station code.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`anet <css3.0-anet_attributes>`    |:ref:`fsta <css3.0-fsta_attributes>`    |:ref:`lddate <css3.0-lddate_attributes>`|:ref:`sta <css3.0-sta_attributes>`      |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`anet <css3.0-anet_attributes>`|:ref:`fsta <css3.0-fsta_attributes>`|
+------------------------------------+------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+----------------------------------+
|:ref:`sta <css3.0-sta_attributes>`|
+----------------------------------+

