from obspy.core import UTCDateTime
from seispy.core import ArgumentError,\
                        DbParsable

class Station(DbParsable):
    '''
    A container class for station data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'sta' in kwargs and 'database' in kwargs:
            _db = kwargs['database']
            _sta = kwargs['sta']
            _dbptr = _db._dbptr
            _tbl_site = _dbptr.lookup(table='site')
            _tbl_site = _tbl_site.subset("sta =~ /{:s}/".format(_sta))
            _tmp = _tbl_site.sort('offdate')
            _tmp.record = _tmp.record_count - 1
            self._offdate = _tmp.getv('offdate')[0]
            _tmp.free()
            _tmp = _tbl_site.sort('ondate')
            _tmp.record = 0
            self._ondate = _tmp.getv('ondate')[0]
            self._blackouts = []
            if _tmp.record_count > 1:
                for _recno in range(_tmp.record_count - 1):
                    _tmp.record = _recno
                    _start = _tmp.getv('offdate')[0]
                    _tmp.record = _recno + 1
                    _stop = _tmp.getv('ondate')[0]
                    self._blackouts += [Blackout(_start, _stop)]
            _tmp.free()
            _tmp = _tbl_site.join('sitechan')
            self.channels = []
            for _record in _tmp.iter_record():
                chan, ondate, offdate = _record.getv('chan', 'ondate', 'offdate')
                self.channels += [Channel(chan=chan, ondate=ondate, offdate=offdate)]
            _tmp.free()

    def is_station_active(self, *args, **kwargs):
        if len(args) == 0:
            raise ArgumentError("at least 1 argument required")
        time = _verify_time_argument(args[0])
        if len(args) == 1:
            if time < self._
            for blackout in self._blackouts:
                if time > blackout.start and time < blackout.stop:
                    return False
            return True
        else:
            start = time
            stop = _verify_time_argument(args[1])
            for blackout in self._blackouts:
                if (start > blackout.start and start < blackout.stop) or\
                        (stop > blackout.start and stop < blackout.stop):
                    return False
            return True

#    def is_channel_active(self, *args, **kwargs):
#        if len(args) == 1:
#            time = args[0]
#            if not isinstance(time, UTCDateTime) and\
#                    not isinstance(time, float) and\
#                    not isinstance(time, int):
#                raise TypeError("invalid type for time argument")
#            if not isinstance(time, UTCDateTime):
#                time = UTCDateTime(time)

class Blackout:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

def _verify_time_argument(time):
    if not isinstance(time, UTCDateTime) and\
            not isinstance(time, float) and\
            not isinstance(time, int):
        raise TypeError("invalid type for time argument")
    if not isinstance(time, UTCDateTime):
        time = UTCDateTime(time)
    return time
