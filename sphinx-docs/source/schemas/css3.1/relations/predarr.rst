.. _css3.1-predarr_relations:

**predarr** -- Earth model predictions of data associated with arrivals
-----------------------------------------------------------------------

This table has information that connects arrival rows to predicted values of related observable based on a particular earth model. It is keyed similar to assoc, but the attributes in this relation are all predicted values based on some earth model. This relations can be thought of as a supplement to assoc that directly stores predicted values of observables rather than residuals. Note that esaz and dip are azimuth and dip of the predicted emergence angle of a given arrival in the focal sphere. esaz is not necessarily the same as that stored in assoc which is conventionally the great circle path angle. Similarly seaz and ema are computed from a model, not from simple spherical geometry.

Fields
^^^^^^

+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`    |:ref:`dip <css3.1-dip_attributes>`      |:ref:`ema <css3.1-ema_attributes>`      |:ref:`esaz <css3.1-esaz_attributes>`    |:ref:`lddate <css3.1-lddate_attributes>`|:ref:`orid <css3.1-orid_attributes>`    |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+
|:ref:`seaz <css3.1-seaz_attributes>`    |:ref:`slow <css3.1-slow_attributes>`    |:ref:`time <css3.1-time_attributes>`    |                                        |                                        |                                        |
+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+----------------------------------------+

Primary Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`|:ref:`orid <css3.1-orid_attributes>`|
+------------------------------------+------------------------------------+

Foreign Keys
^^^^^^^^^^^^

+------------------------------------+------------------------------------+
|:ref:`arid <css3.1-arid_attributes>`|:ref:`orid <css3.1-orid_attributes>`|
+------------------------------------+------------------------------------+

