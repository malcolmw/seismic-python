.. _Id1.0-lastid_relations:

**lastid** -- Counter values (Last value used for keys)
-------------------------------------------------------

This relation is a reference table from which programs may retrieve the last sequential value of one of the numeric keys. Id keys are required before inserting a record in numerous tables. The table has exactly one row for each keyname.

Fields
^^^^^^

+---------------------------------------------+---------------------------------------------+---------------------------------------------+
|:ref:`keyname <Id1.0-keyname_attributes>`    |:ref:`keyvalue <Id1.0-keyvalue_attributes>`  |:ref:`timestamp <Id1.0-timestamp_attributes>`|
+---------------------------------------------+---------------------------------------------+---------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+-----------------------------------------+
|:ref:`keyname <Id1.0-keyname_attributes>`|
+-----------------------------------------+

