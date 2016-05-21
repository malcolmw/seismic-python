import seispy
from seispy import _antelope_defined
__all__ = ["_antelope_defined"]
if seispy._antelope_defined:
    from antelope.datascope import Dbptr,\
                                   dbTABLE_FIELDS
    __all__ += ["Dbptr",
                "dbTABLE_FIELDS"]

#import base classes first
from seispy.core.dbparsable import DbParsable
__all__ += ["DbParsable"]

#import exceptions
from seispy.core.exceptions import ArgumentError,\
                                   InitializationError
__all__ += ["ArgumentError",
            "InitializationError"]

#import subclasses
from seispy.core.arrival import Arrival
from seispy.core.database import Database
from seispy.core.network import Network
from seispy.core.origin import Origin
from seispy.core.station import Station
#from seispy.core.trace import Trace
__all__ += ["Arrival",
            "Database",
            "Network",
            "Origin",
            "Station"]
