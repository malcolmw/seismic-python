.. _dbcluster0.7-volumes_attributes:

**volumes** -- volume segmentation of clustered databases
---------------------------------------------------------

This field gives the boundary intervals for clustered
databases, for example "day", "week", "month", "year", etc.
The first volume is taken to start as specified by the
time field of the clusters relation. If a cluster of
databases has a non-standard start time for its volumes,
an individual row should be used for each database in the
cluster. If there is only one database referenced by
a particular row in the clusters table, the volumes field
may be given as 'single'.

* **Field width:** 30
* **Format:** %-30s
* **Null:** -
