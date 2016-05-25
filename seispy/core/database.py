from seispy.antelope.datascope import dbopen,\
                                      dbSCHEMA_NAME
from seispy.core.iterators import OriginIterator
from seispy.core.virtualnetwork import VirtualNetwork
from seispy.util.schema import Schema

class Database:
    def __init__(self, *args):
        self._dbptr = dbopen(*args)
        self._schema = Schema(schema=self._dbptr.query(dbSCHEMA_NAME))
        _tbl_arrival = self._dbptr.lookup(table='arrival')
        _tmp_view = _tbl_arrival.join('assoc')
        self._srtd_arrival = _tmp_view.sort('orid')
        _tmp_view.free()
        self._grpd_arrival = self._srtd_arrival.group('orid')
        self.vnet = VirtualNetwork(database=self, vnet='ZZ')

    def close(self):
        self._dbptr.close()

    def origins(self, sort_keys=None):
        return OriginIterator(self, sort_keys)
