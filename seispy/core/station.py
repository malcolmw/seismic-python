from seispy.core import *

class Station(DbParsable):
    '''
    A container class for station data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            import os
            import sys
            try:
                sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
                from antelope.datascope import Dbptr,\
                                               dbVIEW_TABLES
            except ImportError:
                #Presumably in the future an alternate parsing method
                #would be implemented for an object other than a Dbptr.
                raise ImportError("$ANTELOPE environment variable not set.")
            if not isinstance(args[0], Dbptr):
                raise TypeError("__init__() received %s in argument position "\
                        "1 (requires antelope.datascope.Dbptr)")
            dbptr = args[0]
            tables = dbptr.query(dbVIEW_TABLES)
            if 'site' not in  tables and 'sitechan' not in tables:
                raise seispy.core.exceptions.InitializationError("Station() "\
                        "constructor needs 'site' and 'sitechan' tables in view")
            self._parse_Dbptr(dbptr)
        else:
            #implement explicit argument specification parsing
            pass
