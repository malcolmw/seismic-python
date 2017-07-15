Fields
======

.. hlist::
  :columns: 6

  * :ref:`arraycode <fields_arraycode>`
  * :ref:`author <fields_author>`
  * :ref:`channel <fields_channel>`
  * :ref:`datatype <fields_datatype>`
  * :ref:`depth <fields_depth>`
  * :ref:`dir <fields_dir>`
  * :ref:`elevation <fields_elevation>`
  * :ref:`file <fields_file>`
  * :ref:`endtime <fields_endtime>`
  * :ref:`eventid <fields_eventid>`
  * :ref:`latitude <fields_latitude>`
  * :ref:`longitude <fields_longitude>`
  * :ref:`narrivals <fields_narrivals>`
  * :ref:`netcode <fields_netcode>`
  * :ref:`nsamples <fields_nsamples>`
  * :ref:`originid <fields_originid>`
  * :ref:`time <fields_time>`
  * :ref:`samplerate <fields_nsamples>`
  * :ref:`stacode <fields_stacode>`

.. _fields_arraycode:

arraycode
---------
  * Description: The array code if the station belongs to an array.
  * Type: TEXT
  * Units: None
  * Range: None

.. _fields_author:

author
------
  * Description: Author.
  * Type: TEXT
  * Units: None
  * Range: None

.. _fields_channel:

channel
-------
  * Description: Data channel.
  * Type: TEXT
  * Units: None
  * Range: None

.. _fields_datatype:

datatype
--------
  * Description: Waveform file format.
  * Type: TEXT
  * Units: none
  * Range: ["MSEED", ...]

.. _fields_depth:

depth
-----
  * Description: Depth below sea-level.
  * Type: REAL
  * Units: km
  * Range: (-inf, inf)

.. _fields_dir:

dir
---
  * Description: Directory path.
  * Type: TEXT
  * Units: none
  * Range: none

.. _fields_elevation:

elevation
---------
  * Description: elevation above sea-level.
  * Type: REAL
  * Units: km
  * Range: (-inf, inf)

.. _fields_endtime:

endtime
-------
  * Description: Epoch/UNIX time (seconds since 00:00:00 01/01/1970).
  * Type: REAL
  * Units: seconds
  * Range: [0, inf)

.. _fields_eventid:

eventid
-------
  * Description: Event ID.
  * Type: INT
  * Units: none
  * Range: (0, inf)

.. _fields_file:

file
----
  * Description: File name.
  * Type: TEXT
  * Units: none
  * Range: none

.. _fields_latitude:

latitude
--------
  * Description: Latitude.
  * Type: REAL
  * Units: Degrees
  * Range: [-90, 90]

.. _fields_longitude:

longitude
---------
  * Description: Longitude.
  * Type: REAL
  * Units: Degrees
  * Range: [-180, 360]

.. _fields_narrivals:

narrivals
---------
  * Description: Number of associated arrivals.
  * Type: INT
  * Units: none
  * Range: [0, inf)

.. _fields_netcode:

netcode
-------
  * Description: Network code.
  * Type: TEXT
  * Units: none
  * Range: none

.. _fields_nsamples:

nsamples
--------
  * Description: Number of data samples in file.
  * Type: INT
  * Units: none
  * Range: [1, inf)

.. _fields_originid:

originid
--------
  * Description: Origin ID.
  * Type: INT
  * Units: none
  * Range: [0, inf)

.. _fields_time:

time
----
  * Description: Epoch/UNIX time (seconds since 00:00:00 01/01/1970).
  * Type: REAL
  * Units: seconds
  * Range: [0, inf)

.. _fields_samplerate:

samplerate
----------
  * Description: Data sampling rate.
  * Type: REAL
  * Units: Hz, sps
  * Range: (0, inf)

.. _fields_stacode:

stacode
-------
  * Description: Station code.
  * Type: TEXT
  * Units: none
  * Range: none
