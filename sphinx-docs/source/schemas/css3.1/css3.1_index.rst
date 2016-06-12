.. _css3.1_schema_index:

**css3.1** -- Center for Seismic Studies Schema Version 3.1 extended
====================================================================

.. toctree::
   :hidden:

   attributes/attributes_index_all
   relations/relations_index_all

Attributes
----------

:ref:`A <css3.1_attributes_index_A>` | :ref:`B <css3.1_attributes_index_B>` | :ref:`C <css3.1_attributes_index_C>` | :ref:`D <css3.1_attributes_index_D>` | :ref:`E <css3.1_attributes_index_E>` | :ref:`F <css3.1_attributes_index_F>` | :ref:`G <css3.1_attributes_index_G>` | :ref:`H <css3.1_attributes_index_H>` | :ref:`I <css3.1_attributes_index_I>` | :ref:`J <css3.1_attributes_index_J>` | :ref:`K <css3.1_attributes_index_K>` | :ref:`L <css3.1_attributes_index_L>` | :ref:`M <css3.1_attributes_index_M>` | :ref:`N <css3.1_attributes_index_N>` | :ref:`O <css3.1_attributes_index_O>` | :ref:`P <css3.1_attributes_index_P>` | :ref:`Q <css3.1_attributes_index_Q>` | :ref:`R <css3.1_attributes_index_R>` | :ref:`S <css3.1_attributes_index_S>` | :ref:`T <css3.1_attributes_index_T>` | :ref:`U <css3.1_attributes_index_U>` | :ref:`V <css3.1_attributes_index_V>` | :ref:`W <css3.1_attributes_index_W>` | :ref:`all <css3.1_attributes_index_all>`

Relations
---------

:ref:`A <css3.1_relations_index_A>` | :ref:`B <css3.1_relations_index_B>` | :ref:`C <css3.1_relations_index_C>` | :ref:`E <css3.1_relations_index_E>` | :ref:`F <css3.1_relations_index_F>` | :ref:`G <css3.1_relations_index_G>` | :ref:`I <css3.1_relations_index_I>` | :ref:`L <css3.1_relations_index_L>` | :ref:`M <css3.1_relations_index_M>` | :ref:`N <css3.1_relations_index_N>` | :ref:`O <css3.1_relations_index_O>` | :ref:`P <css3.1_relations_index_P>` | :ref:`R <css3.1_relations_index_R>` | :ref:`S <css3.1_relations_index_S>` | :ref:`W <css3.1_relations_index_W>` | :ref:`all <css3.1_relations_index_all>`

Detail
------

css3.1 is derived from the original CSS3.0 schema, and is mostly
		unchanged.  However, many fields were increased in size to better
		accommodate larger databases.  The flat-file format of a database with
		this schema is therefore no longer compatible with the css3.0 schema.
		The following changes were made:

		* All "id" fields changed from 8 to 12 character integers.
		* deast and dnorth are %10.5f floats (rather than %9.4f)
		* dfile is 48 chars (instead of 32)
		* dir is 80 chars (instead of 64)
		* grname and srname are 64 chars (instead of 40)
		* nass and ndef are 5 character ints (instead of 4)
		* nsamp is 12 character int (instead of 8)
		* segtype is 8 chars (instead of 2)
		* samprate is %14.7f (instead of %11.7f)
		* sta is 14 chars (instead of 6)
		* chan is 15 chars (instead of 8)
		* evname is 50 (instead of 15)
		* auth is 30 (instead of 15)
		* vmodel is 30 (instead of 15)
		* lat & lon are %12.7f floats (instead of %9.4f)
		* change time resolution from 10 usec to 1 usec
		* add prefmag attribute to event table
		* add pfdisc relation

		Modifications from original CSS documentation:

		0) units of calib vary according to the instrument, with wfdisc.segtype and instrument.rsptype indicating both sensor type and units
		1) Null values corrected for certain attributes.
		2) offdate added to primary keys for tables in which it occurs.
		3) endtime added to primary keys for tables in which it occurs.
		4) time made first primary key in origin for sorting.
		5) arid and orid added to foreign keys in assoc.
		6) made range values expression for automated testing
		7) added wfedit relation 12/3/93
		8) changed the primary key in sitechan to chanid, and added chanid as a foreign key in sensor to force joins of sitechan to go through sensor table.
		9) changed primary keys in moment and centryd table to orid.
		10) added calibration and stage tables 1/31/94
		11) changed primary keys in stamag to arid, magtype, sta, orid
		12) changed primary key in site to sta (no ondate, offdate)
		13) changed null values for origerr's covariant matrix
		14) changed definition of ndef for origins included from other catalogs
		15) added beam, fkgrid and stgrid tables to accomodate array processing 12/15/94
		16) added wftar table to accomodate tar tape waveform archiving 1/9/95
		17) changed all NONULL null values to reasonable values
		18) added wfrms table
		19) added wfmeas table for holding generic waveform measurements
		20) segment origin and stassoc etype field into two fields, etype and review, so that analyst review status can be kept in origin table
		21) add snetsta, anetsta, schanloc and achanaux tables to translate between foreign volumes of SEED or autoDRM into local databases.
		22) add specdisc table and associated attributes to support spectral estimation processing
		23) add rsprm to specdisc table
		24) added tables dmcseed and dmcwf to database to support all the DMC requirements for building DMC seed volumes.  Changed default value of fileno to -1.
		25) changed format of chksum from Integer %15ld to Real %12.0f to make sure table is written properly.  Previous format would wrap to negative numbers in some cases which would corrupt the database.
		26) added fields calib, calper, samprate, timever to table dmcwf and field totbytes to table dmcseed.
		27) changed primary keys of stamag from arid magtype sta and orid to magid magtype sta and orid.
		28) changed fields dmcseedfile to dfile and jdate to yearday in tables dmcwf and dmcseed.
		29) added focal mechanism calculation related tables and emodel table
		30) extensive changes to wfrms table to make compatible with orbwfrms
		31) made instrument table alternate key all fields except inid and lddate
		32) introduced new calibration table, with new fields samprate, segtype, dlsta, dlchan, and lead.
		33) changed primary keys of origin to include ndef and nass
		34) made new table mt to hold moment tensor solutions as reported by USGS GeoJSON data feed
