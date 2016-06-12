.. _Trace4.1-evid_attributes:

**evid** -- event id
--------------------

Each event is assigned a unique positive
integer which identifies it in a database. It is possible
for several records in the origin relation to have the same
evid. This indicates there are several opinions about the
location of the event.

* **Field width:** 12
* **Format:** %12ld
* **Null:** -1
* **Range:** evid > 0
