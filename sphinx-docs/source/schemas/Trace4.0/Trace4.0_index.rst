.. _Trace4.0_schema_index:

**Trace4.0** -- Trace Manipulation and Processing Database
==========================================================

.. toctree::
   :hidden:

   attributes/attributes_index_all
   relations/relations_index_all

Attributes
----------

:ref:`A <Trace4.0_attributes_index_A>` | :ref:`B <Trace4.0_attributes_index_B>` | :ref:`C <Trace4.0_attributes_index_C>` | :ref:`D <Trace4.0_attributes_index_D>` | :ref:`E <Trace4.0_attributes_index_E>` | :ref:`F <Trace4.0_attributes_index_F>` | :ref:`G <Trace4.0_attributes_index_G>` | :ref:`H <Trace4.0_attributes_index_H>` | :ref:`I <Trace4.0_attributes_index_I>` | :ref:`J <Trace4.0_attributes_index_J>` | :ref:`K <Trace4.0_attributes_index_K>` | :ref:`L <Trace4.0_attributes_index_L>` | :ref:`M <Trace4.0_attributes_index_M>` | :ref:`N <Trace4.0_attributes_index_N>` | :ref:`O <Trace4.0_attributes_index_O>` | :ref:`P <Trace4.0_attributes_index_P>` | :ref:`Q <Trace4.0_attributes_index_Q>` | :ref:`R <Trace4.0_attributes_index_R>` | :ref:`S <Trace4.0_attributes_index_S>` | :ref:`T <Trace4.0_attributes_index_T>` | :ref:`U <Trace4.0_attributes_index_U>` | :ref:`V <Trace4.0_attributes_index_V>` | :ref:`W <Trace4.0_attributes_index_W>` | :ref:`all <Trace4.0_attributes_index_all>`

Relations
---------

:ref:`A <Trace4.0_relations_index_A>` | :ref:`E <Trace4.0_relations_index_E>` | :ref:`H <Trace4.0_relations_index_H>` | :ref:`L <Trace4.0_relations_index_L>` | :ref:`M <Trace4.0_relations_index_M>` | :ref:`T <Trace4.0_relations_index_T>` | :ref:`all <Trace4.0_relations_index_all>`

Detail
------

This deprecated schema provides the parameter
		information needed during standard processing of
		seismic waveform data.  It has been replaced with
		Trace4.1.

		It is largely derived from the CSS 3.0 database,
		with additions which address specific trace manipulation
		issues, and the representation of traces in memory.
		The information contained in the central
		trace relation represents a join of many tables,
		in particular wfdisc, site, sitechan, sensor and instrument.
