from seispy.core import Event,\
                        Origin
from seispy.antelope.datascope import dbTABLE_IS_VIEW
class EventIterator:
    def __init__(self, database):
        self._database = database
        self._tbl_event = database._dbptr.lookup(table='event')
        self._tbl_event.record = 0

    def __iter__(self):
        return self

    def next(self):
        if self._tbl_event.record == self._tbl_event.record_count:
            raise StopIteration
        _event = Event(evid=self._tbl_event.getv('evid')[0],
                       database=database)
        self._tbl_event.record += 1
        return _event

class OriginIterator:
    def __init__(self, database, sort_keys):
        self._database = database
        if sort_keys:
            for key in sort_keys:
                if key not in ('lat',
                            'lon',
                            'depth',
                            'time',
                            'orid',
                            'evid',
                            'jdate',
                            'nass',
                            'ndef',
                            'grn',
                            'srn',
                            'dtype',
                            'algorithm',
                            'auth'):
                    raise ValueError("invalid value for sort_keys keyword "\
                            "argument")
        self._tbl_origin = database._dbptr.lookup(table='origin')
        if sort_keys:
            self._tbl_origin = self._tbl_origin.sort(sort_keys)
        self._tbl_origin.record = 0

    def __iter__(self):
        return self

    def next(self):
        if self._tbl_origin.record == self._tbl_origin.record_count:
            if self._tbl_origin.dbTABLE_IS_VIEW:
                self._tbl_origin.close()
            raise StopIteration
        _origin = Origin(orid=self._tbl_origin.getv('orid')[0],
                      database=self._database)
        self._tbl_origin.record += 1
        return _origin
