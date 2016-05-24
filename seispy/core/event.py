from seispy.core import DbParsable,\
                        Origin

class Event(DbParsable):
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        elif 'evid' in kwargs and 'database' in kwargs:
            _db = kwargs['database']
            _evid = kwargs['evid']
            _dbptr = _db._dbptr
            _tbl_event = _dbptr.lookup(table='event')
            _tbl_event.record = _tbl_event.find("evid == {:d}".format(_evid))
            self._parse_Dbptr(_tbl_event.record)
            _tbl_origin = _dbptr.lookup(table='origin')
            _tbl_origin = _tbl_origin.subset("evid == {:d}".format(_evid))
            self.origins = []
            for origin in _tbl_origin.iter_record():
                self.origins += [Origin(database=_db, orid=origin.getv('orid')[0])]
            self.attributes += ('origins',)
