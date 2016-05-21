from seispy.core import *

class DbParsable:
    def __init__(self, *args, **kwargs):
        print (__package__)
        pass

    def __str__(self):
        ret = "{} Instance".format(self.__class__)
        ret += "\n" + "-" * (len(str(self.__class__)) + 8) + "\n"
        width = max([len(attr) for attr in self.attributes]) + 1
        for attr in self.attributes:
            ret += "{:<{width}s} {}\n".format((attr + ':'),
                                             getattr(self, attr),
                                             width=width)
        return ret.rstrip()

    def _parse_Dbptr(self, dbptr):
        if not _antelope_defined:
            raise InitializationError("Antelope environment not initialized")
        if not isinstance(dbptr, Dbptr):
            raise TypeError("expected antelope.datascope.Dbptr instance")
        if dbptr.record < 0 or dbptr.record >= dbptr.record_count:
            raise IndexError("invalid record index in antelope.datascope.Dbptr")
        #do some class specific error checking
        if self.__class__ == 'seispy.core.arrival.Arrival':
            pass
        if self.__class__ == 'seispy.core.origin.Origin':
            pass
        if self.__class__ == 'seispy.core.network.Network':
            pass
        if self.__class__ == 'seispy.core.station.Station':
            if dbptr.query(dbVIEW_TABLES) != ('site', 'sitechan') and\
                    dbptr.query(dbVIEW_TABLES) != ('sitechan', 'site'):
                raise InitializationError("view must be comprised of 'site' "\
                        "and 'sitechan' tables only")
        if self.__class__ == 'seispy.core.trace.Trace':
            pass
        for field in dbptr.query(dbTABLE_FIELDS):
            setattr(self, field, dbptr.getv(field)[0])
            self.attributes += (field,)
        self.name = self.sta
