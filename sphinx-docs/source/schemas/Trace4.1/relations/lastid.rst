.. _Trace4.1-lastid_relations:

**lastid** -- Counter values (Last value used for keys)
-------------------------------------------------------

This relation is a reference table from which programs may retrieve the last sequential value of one of the numeric keys. Unique keys are required before inserting a record in numerous tables. The table has exactly one row for each keyname. In the core schema there are just 9 distinct identifier keys: arid, chanid, commid, evid, inid, magid, orid, stassid, wfid. This table will also support application-specific keys as needed. Users are encouraged to use the dbgetcounter library routine to obtain a counter value.

Fields
^^^^^^

+----------------------------------------------+----------------------------------------------+
|:ref:`keyname <Trace4.1-keyname_attributes>`  |:ref:`keyvalue <Trace4.1-keyvalue_attributes>`|
+----------------------------------------------+----------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------+
|:ref:`keyname <Trace4.1-keyname_attributes>`|
+--------------------------------------------+

