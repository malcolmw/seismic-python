.. _css3.0-snetsta_relations:

**snetsta** -- map seed net+sta code to local sta code
------------------------------------------------------

SEED and autoDRM use network to further specify station, but the css3.0 schema doesn't support net as a key whereever sta is used. This table maps foreign seed net+sta codes to a unique local station code.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`fsta <css3.0-fsta_attributes>`    |:ref:`lddate <css3.0-lddate_attributes>`|:ref:`snet <css3.0-snet_attributes>`    |:ref:`sta <css3.0-sta_attributes>`      |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+----------------------------------+
|:ref:`sta <css3.0-sta_attributes>`|
+----------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`fsta <css3.0-fsta_attributes>`|:ref:`snet <css3.0-snet_attributes>`|
+------------------------------------+------------------------------------+

