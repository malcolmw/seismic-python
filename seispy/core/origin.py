from seispy.core import *
class Origin(DbParsable):
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            import os
            import sys
            try:
                sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
            except ImportError:
                #Presumably in the future an alternate parsing method
                #would be implemented for an object other than a Dbptr.
                raise ImportError("$ANTELOPE environment variable not set.")
            self._parse_Dbptr(args[0])
        elif len(args) == 4:
            self.lat = args[0]
            self.lon = args[1]
            self.depth = args[2]
            self.time = args[3]
            self.attributes += ('lat', 'lon', 'depth', 'time')
            for attr in ('orid', 'evid', 'jdate', 'nass', 'ndef', 'arrivals'):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)
        else:
            raise TypeError("__init__() takes exactly 1 or 5 arguments ({:d} "\
                    "given)".format(len(args)))

    def __str__(self):
        ret = "Origin Object\n-------------\n"
        for attr in self.attributes:
            ret += "{:<14s}{}\n".format((attr + ':'), getattr(self, attr))
        return ret.rstrip()
