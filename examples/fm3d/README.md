Example
=======

This is an example of how to generate travel-times and ray-paths.

Update the configuration file to point to the correct data files.

>[General]
>velocity_model = .../examples/fm3d/VpVs.dat
>topography = .../examples/fm3d/anza.xyz
>stations = .../examples/fm3d/stations.dat
>h0 =	5.0	#grid origin height above sea-level
>lon0 =	241.83	#grid origin longitude
>lat0 =	32.38	#grid origin latitude
>dr =	1.0	#grid node interval along radial axis
>dlon =	0.01	#grid node interval along longitudinal axis
>dlat =	0.01	#grid node interval along latitudinal axis
>nr =	36	#number of grid nodes along radial axis
>nlon =	278	#number of grid nodes along longitudinal axis
>nlat =	218	#number of grid nodes along latitudinal axis

Then execute:
```bash
bash>$ fm3d_ttimes fm3d_ttimes.cfg
```
