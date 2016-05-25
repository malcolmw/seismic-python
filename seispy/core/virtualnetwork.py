from seispy.core.exceptions import InitializationError
from seispy.core.network import Network

class VirtualNetwork:
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if 'database' in kwargs and 'vnet' in kwargs:
            db = kwargs['database']
            self.vnet = kwargs['database']
            self.attributes += ('vnet',)
            tbl_snetsta = db._dbptr.lookup(table='snetsta')
            tbl_snetsta = tbl_snetsta.sort('snet', unique=True)
            self.subnets = ()
            for record in tbl_snetsta.iter_record():
                self.subnets += (Network(database=db,
                                          net=record.getv('snet')[0]),)
            tbl_snetsta.free()
            self.attributes += ('subnets',)
        else:
            raise InitializationError("specify 'database' and 'vnet' keyword "\
                    "arguments")
