from seispy.core.exceptions import InitializationError
from seispy.core.station import Station

class Network:
    '''
    A container class for network data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'net' in kwargs and 'database' in kwargs:
            self.net = kwargs['net']
            self.attributes += ('net',)
            db = kwargs['database']
            dbptr = db._dbptr
            tbl_snetsta = dbptr.lookup(table='snetsta')
            tbl_snetsta = tbl_snetsta.subset("snet =~ /{:s}/".format(self.net))
            self.stations = ()
            for record in tbl_snetsta.iter_record():
                sta = record.getv('sta')[0]
                try:
                    self.stations += (Station(database=db, sta=sta),)
                except InitializationError as err:
                    print err.message
            self.attributes += ('stations',)
            tbl_snetsta.free()
        else:
            #implement explicit argument specification parsing
            raise InitializationError("specify 'net' and 'database' keyword "\
                    "arguments")
