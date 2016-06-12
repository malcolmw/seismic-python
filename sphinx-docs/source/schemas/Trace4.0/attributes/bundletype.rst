.. _Trace4.0-bundletype_attributes:

**bundletype** -- type of bundle
--------------------------------

The bundle type is an arbitrary integer which specifies
the kind of the bundle.  A few standard types are defined:
0 -- waveform segment (single trace)
1 -- time-ordered waveform segments for single channel
2 -- waveforms grouped by component
3 -- waveforms grouped by station
4 -- waveforms grouped by array
5 -- waveforms grouped by network

* **Field width:** 20
* **Format:** %20ld
