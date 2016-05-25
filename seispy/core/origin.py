from seispy.core.arrival import Arrival
from seispy.core.dbparsable import DbParsable

class Origin(DbParsable):
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
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
        elif 'orid' in kwargs and 'database' in kwargs:
            _db = kwargs['database']
            _orid = kwargs['orid']
            _dbptr = _db._dbptr
            _tbl_origin = _dbptr.lookup(table='origin')
            _tbl_origin.record = _tbl_origin.find("orid == {:d}".format(_orid))
            self._parse_Dbptr(_tbl_origin)
            _grpd_arrival = _db._grpd_arrival
            _grpd_arrival.record = _grpd_arrival.find("orid == "\
                    "{:d}".format(_orid))
            self.arrivals = []
            _srtd_arrival = _db._srtd_arrival
            start, end = _grpd_arrival.get_range()
            for _srtd_arrival.record in range(start, end):
                self.arrivals += [Arrival(_srtd_arrival)]
            self.attributes += ('arrivals',)

        else:
            raise TypeError("__init__() takes exactly 1 or 5 arguments ({:d} "\
                    "given)".format(len(args)))
