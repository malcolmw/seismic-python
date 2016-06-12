.. _css3.1-lastid_relations:

**lastid** -- Counter values (Last value used for keys)
-------------------------------------------------------

This relation is a reference table from which programs may retrieve the last sequential value of one of the numeric keys. Id keys are required before inserting a record in numerous tables. The table has exactly one row for each keyname. In the core schema there are just 9 distinct identifier keys: arid, chanid, commid, evid, inid, magid, orid, stassid, wfid. This table will also support application-specific keys, provided they are defined by some table. Users are encouraged to use the dbnextid library routine or command to obtain a unique counter value.

Fields
^^^^^^

+--------------------------------------------+--------------------------------------------+--------------------------------------------+
|:ref:`keyname <css3.1-keyname_attributes>`  |:ref:`keyvalue <css3.1-keyvalue_attributes>`|:ref:`lddate <css3.1-lddate_attributes>`    |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------------+
|:ref:`keyname <css3.1-keyname_attributes>`|
+------------------------------------------+

