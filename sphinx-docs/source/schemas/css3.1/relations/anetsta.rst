.. _css3.1-anetsta_relations:

**anetsta** -- map autodrm net+sta code to local sta code
---------------------------------------------------------

SEED and autoDRM use network to further specify station, but the css3.1 schema doesn't support net as a key whereever sta is used. This table maps foreign autodrm net+sta codes to a unique local station code.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`anet <css3.1-anet_attributes>`    |:ref:`fsta <css3.1-fsta_attributes>`    |:ref:`lddate <css3.1-lddate_attributes>`|:ref:`sta <css3.1-sta_attributes>`      |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`anet <css3.1-anet_attributes>`|:ref:`fsta <css3.1-fsta_attributes>`|
+------------------------------------+------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+----------------------------------+
|:ref:`sta <css3.1-sta_attributes>`|
+----------------------------------+

