from seispy.core import DbParsable

class Station(DbParsable):
    '''
    A container class for station data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            if not _antelope_defined:
                raise InitializationError("Antelope environment not initialized")
            dbptr = args[0]
            tables = dbptr.query(dbVIEW_TABLES)
            if tables != ('site', 'sitechan') and tables != ('sitechan', 'site'):
                raise InitializationError("seispy.antelope.datascope.Dbptr "\
                        "object passed to seispy.core.station.Station "\
                        "constructor must point to 'site' and 'sitechan' "\
                        "tables only")
            if dbptr.record < 0 or dbptr.record >= dbptr.record_count:
                raise InitializationError("seispy.antelope.datascope.Dbptr "\
                        "object passed to seispy.core.station.Station "\
                        "constructor must point to valid record")
            sta, ondate, offdate, lat, lon, elev = dbptr.getv('sta',
                                                              'ondate',
                                                              'offdate',
                                                              'lat',
                                                              'lon',
                                                              'elev')
            dbptr.record = -1
            chans = ()
            while True:
                try:
                    dbptr.record = dbptr.find("sta =~ /{:s}/ && ondate <= "\
                            "{:d} && offdate >= {:d}".format(sta,
                                                             ondate,
                                                             offdate),
                                              first=dbptr.record)
                except DbfindEnd:
                    break
                chans += (dbptr.getv('chan')[0])
            self._parse_kwargs({"sta": sta,
                                "ondate": ondate,
                                "offdate": offdate,
                                "lat": lat,
                                "lon": lon,
                                "elev": elev,
                                "chans": chans})

        else:
            self._parse_kwargs(kwargs)
