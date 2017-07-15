fm3d
====
A module to provide I/O functionality for files formatted for input to FM3D.

.. module:: fm3d

Public functions
----------------

.. function:: generate_ttgrid(vel_mod, stations, phase, grid)

  :param `seispy.velocity.VelocityModel` vel_mod: Velocity model to use for
                                                  calculating travel-times.
  :param list stations: List of `seispy.metadata.Station` objects. Calculate
                        travel-times to these stations.
  :param str phase: Seismic phase to calculate travel-times for ["P", "S", "Vp", Vs"].
  :param dict grid: Dictionary of grid parameters. Calculate node-to-station
                    travel-times for nodes on the grid. Click
                    :ref:`here <fm3d.grid_parameters>` for an explanation of the
                    grid parameters.

.. _fm3d.grid_parameters:

Grid parameters
~~~~~~~~~~~~~~~

  * **lat0**: Grid origin latitude [degrees].
  * **lon0**: Grid origin longitude [degrees].
  * **h0**: Grid origin elevation (above surface) [km].
  * **dlat**: Grid node interval along latitudinal axis [degrees].
  * **dlon**: Grid node interval along longitudinal axis [degrees].
  * **dr**: Grid node interval along depth axis [km].
  * **nlat**: Number of grid nodes along latitudinal axis.
  * **nlon**: Number of grid nodes along longitudinal axis.
  * **nr**: Number of grid nodes along depth axis.

