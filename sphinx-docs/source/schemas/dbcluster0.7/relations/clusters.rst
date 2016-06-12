.. _dbcluster0.7-clusters_relations:

**clusters** -- database clusters
---------------------------------

This table defines clusters of databases. Each row may specify one single database of a particular type (indicated by clustername, for example a master_stations database), or a collection of databases with a regular naming convention. The time and endtime specify the time range covered by the entire cluster (endtime may be left null for open-ended clusters). The specific database name for each database in a cluster may be derived based on percent-escape sequences in the dir and dfile fields.

Fields
^^^^^^

+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
|:ref:`clustername <dbcluster0.7-clustername_attributes>`|:ref:`dbmachine <dbcluster0.7-dbmachine_attributes>`    |:ref:`description <dbcluster0.7-description_attributes>`|:ref:`dfile <dbcluster0.7-dfile_attributes>`            |:ref:`dir <dbcluster0.7-dir_attributes>`                |:ref:`endtime <dbcluster0.7-endtime_attributes>`        |
+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+
|:ref:`lddate <dbcluster0.7-lddate_attributes>`          |:ref:`net <dbcluster0.7-net_attributes>`                |:ref:`schema <dbcluster0.7-schema_attributes>`          |:ref:`time <dbcluster0.7-time_attributes>`              |:ref:`volumes <dbcluster0.7-volumes_attributes>`        |                                                        |
+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+--------------------------------------------------------+

Primary Keys
^^^^^^^^^^^^

+--------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+
|:ref:`clustername <dbcluster0.7-clustername_attributes>`                                    |:ref:`time <dbcluster0.7-time_attributes>`:::ref:`endtime <dbcluster0.7-endtime_attributes>`|
+--------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+

Alternate Keys
^^^^^^^^^^^^^^

+--------------------------------------------+--------------------------------------------+
|:ref:`dfile <dbcluster0.7-dfile_attributes>`|:ref:`dir <dbcluster0.7-dir_attributes>`    |
+--------------------------------------------+--------------------------------------------+

