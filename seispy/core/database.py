from seispy.core import OriginIterator
from seispy.antelope.datascope import dbopen

class Database:
    def __init__(self, *args):
        self._dbptr = dbopen(*args)
        _tbl_arrival = self._dbptr.lookup(table='arrival')
        _tmp_view = _tbl_arrival.join('assoc')
        self._srtd_arrival = _tmp_view.sort('orid')
        _tmp_view.free()
        self._grpd_arrival = self._srtd_arrival.group('orid')

    def close(self):
        self._dbptr.close()

    def origins(self, sort_keys=None):
        return OriginIterator(self, sort_keys)
