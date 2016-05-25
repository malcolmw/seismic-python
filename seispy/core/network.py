from seispy.core.dbparsable import DbParsable

class Network(DbParsable):
    '''
    A container class for network data.
    '''
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
        else:
            #implement explicit argument specification parsing
            pass
