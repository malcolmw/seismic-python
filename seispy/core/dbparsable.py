from seispy import _antelope_defined
from seispy.core.exceptions import InitializationError
from seispy.antelope.datascope import Dbptr,\
                                      dbTABLE_FIELDS

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
            print type(dbptr), dbptr.__class__
            raise TypeError("expected antelope.datascope.Dbptr instance")
        if dbptr.record < 0 or dbptr.record >= dbptr.record_count:
            raise IndexError("invalid record index in antelope.datascope.Dbptr")
        for field in dbptr.query(dbTABLE_FIELDS):
            if field not in self.attributes:
                setattr(self, field, dbptr.getv(field)[0])
                self.attributes += (field,)

    def _parse_kwargs(self, kwargs):
        for kw in primary_kwargs:
            if kw not in kwargs:
                raise InitializationError("keywords {} required for "\
                        "{:s}()".format(primary_kwargs, self.__class__))
            for kw in valid_kwargs:
                if kw in kwargs:
                    setattr(self, attr, kwargs[kw])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)

