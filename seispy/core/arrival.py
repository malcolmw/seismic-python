from seispy.core.dbparsable import DbParsable
from seispy.core.exceptions import InitializationError

class Arrival(DbParsable):
    """
    The Arrival class is a container class for phase arrival data and
    can be initialized one of two ways.


    1. Specifying a series of keyword arguments initializing individual
       fields. If initializating via keyword arguments primary keys
       *sta*, *time*, and *iphase* must be specified.

    **OR**

    2. Passing in a seispy.antelope.datascope.Dbptr object that points
       to a record in an *arrival* table.

    The second method of initialization is intended primarily for
    internal use within the seispy package.

    :argument seispy.antelope.datascope.Dbptr args: Database pointer\
    to record in *arrival* table
    :keyword str sta: Station code
    :keyword float time: Arrival time
    :keyword str iphase: Interpreted phase
    :keyword str chan: Channel code
    :keyword float deltim: Arrival timing error
    :keyword float qual: Pick quality ('i'=impulsive, 'e'=emergent,\
    'w'=weak)
    :raise InitializationError: if initialization method\
    2. is used and primary keys (*sta*, *time*, and *iphase*) are not\
    specified.
    :raise TypeError: sometimes

    .. code-block:: python

       >>> from seispy.core import Arrival
       >>> arrival = Arrival(sta='MCAW',
                             time=597645900.000,
                             iphase="P",
                             chan="HHZ",
                             deltim=0.2)

    .. versionadded:: 0.0alpha
    .. codeauthor:: Malcolm White mcwhite@ucsd.edu
    """
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        else:
            primary_kwargs = ('sta', 'time', 'iphase')
            for kw in primary_kwargs:
                if kw not in kwargs:
                    raise InitializationError("must specify 'sta', 'time', "\
                            "and 'iphase' for Arrival")
            valid_kwargs = ('sta',
                            'time',
                            'arid',
                            'jdate',
                            'stassid',
                            'chanid',
                            'chan',
                            'iphase',
                            'stype',
                            'deltim',
                            'azimuth',
                            'delaz',
                            'slow',
                            'delslo',
                            'ema',
                            'rect',
                            'amp',
                            'per',
                            'logat',
                            'clip',
                            'fm',
                            'snr',
                            'qual',
                            'auth',
                            'commid',
                            'lddate')
            for kw in valid_kwargs:
                if kw in kwargs:
                    setattr(self, attr, kwargs[kw])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)

