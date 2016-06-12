.. _Trace4.0-evid_attributes:

**evid** -- event id
--------------------

Each event is assigned a unique positive
integer which identifies it in a database. It is possible
for several records in the origin relation to have the same
evid. This indicates there are several opinions about the
location of the event.

* **Field width:** 8
* **Format:** %8ld
* **Null:** -1
* **Range:** evid > 0
