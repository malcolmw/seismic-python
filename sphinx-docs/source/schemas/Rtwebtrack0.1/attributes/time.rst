.. _Rtwebtrack0.1-time_attributes:

**time** -- time of a web event
-------------------------------

The time field gives the Unix epoch time corresponding
to a particular web event. In the case of web requests,
this is the time of the last request for the given
url from the given peer.

* **Field width:** 17
* **Format:** %17.5f
* **Null:** -9999999.99999
* **Units:** seconds
