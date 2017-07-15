TTGrid - Travel-Time Grid
=========================

A class to contain and provide queryable access to source-to-station 
travel-time information.

Constructor
-----------

.. class:: seispy.ttgrid.TTGrid()

Public methods
--------------

Storage - .ttg file format
--------------------------
* **Header** - *ASCII format*

  * Line 1: Phase type (P or S)
  * Line 2: Grid origin coordinates

    * Latitude [degrees]
    * Longitude [degrees]
    * Depth [km]

  * Line 3: Grid node intervals

    * Column 1: Grid node spacing along latitudinal axis [degrees]
    * Column 2: Grid node spacing along longitudinal axis [degrees]
    * Column 3: Grid node spacing along depth axis [degrees]

  * Line 4: Number of grid nodes

    * Column 1: Number of grid nodes along latitudinal axis
    * Column 2: Number of grid nodes along longitudinal axis
    * Column 3: Number of grid nodes along depth axis

  * Line 5: Number of stations
  * Lines 6+: Station metadata (1 line per station)

    * Column 1: Station code
    * Column 2: Station latitude [degrees]
    * Column 3: Station longitude [degrees]
    * Column 4: Station elevation [km]

* **Body** - *Binary format*

  * 1 block per station listed on lines 6+. Blocks in same order as stations
    listed on lines 6+.

    * 4-byte floating-point travel-times of node-to-station travel-times. First
      value corresponds to origin node. Node coordinates vary fastest along
      latitudinal axis and slowest along depth axis.
