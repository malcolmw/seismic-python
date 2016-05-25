from os.path import isfile
from obspy.core.trace import Trace as ObspyTrace
from obspy.core import read,\
                       Stream,\
                       UTCDateTime
from seispy.core.exceptions import ArgumentError,\
                                   InitializationError

class Trace(ObspyTrace):
    '''
    Convenience class to create an obspy.core.trace.Trace-like object.
    '''
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], str) and isfile(args[0]):
                tr = read(args[0])[0]
                self.stats = tr.stats
                self.data = tr.data
            else:
                try:
                    import os
                    import sys
                    sys.path.append("{:s}/data/python".format(os.environ['ANTELOPE']))
                except ImportError:
                    raise ImportError("$ANTELOPE environment variable not defined")
                from antelope.datascope import Dbptr,\
                                            dbTABLE_NAME
                if isinstance(args[0], Dbptr):
                    dbptr = args[0]
                    if dbptr.query(dbTABLE_NAME) == 'wfdisc':
                        if dbptr.record >= 0 and dbptr.record < dbptr.record_count:
                            tr = read(dbptr.filename()[1])[0]
                            self.stats = tr.stats
                            self.data = tr.data
                        else:
                            raise ValueError("Dbptr.record out of range")
                    else:
                        raise ValueError("Dbptr argument received by "\
                                "__init__() must point to 'wfdisc' table "\
                                "(Dbptr points to '{:s}' table)".format(dbptr.query(dbTABLE_NAME)))
                else:
                    raise TypeError("Unable to process single argument passed "\
                            "to __init__(): {:s}".format(args[0]))
        else:
            if 'station' not in kwargs or\
                    'channel' not in kwargs or\
                    'starttime' not in kwargs or\
                    'endtime' not in kwargs:
                raise ArgumentError("__init__() expected 'station', 'channel',"\
                        " 'starttime' and 'endtime' keyword arguments")
            if not isinstance(kwargs['starttime'], UTCDateTime) and\
                    not isinstance(kwargs['starttime'], float) and\
                    not isinstance(kwargs['starttime'], int):
                raise TypeError("__init__() keyword argument 'starttime' must "\
                        "be of type 'UTCDateTime', 'float' or 'int'")
            if not isinstance(kwargs['endtime'], UTCDateTime) and\
                   not isinstance(kwargs['endtime'], float) and\
                    not isinstance(kwargs['endtime'], int):
                raise TypeError("__init__() keyword argument 'endtime' must "\
                        "be of type 'UTCDateTime', 'float' or 'int'")
            if not isinstance(kwargs['station'], str):
                raise TypeError("__init__() keyword argument 'station' must "\
                        "be of type 'str'")
            if not isinstance(kwargs['channel'], str):
                raise TypeError("__init__() keyword argument 'channel' must "\
                        "be of type 'str'")
            if 'database_path' in kwargs:
                if not isfile("{:s}.wfdisc".format(kwargs['database_path'])):
                    raise InitializationError("wfdisc does not exist "\
                            "{:s}.wfdisc".format(kwargs['database_path']))
                import os
                import sys
                try:
                    sys.path.append("{:s}/data/python".format(os.environ['ANTELOPE']))
                except ImportError:
                    raise ImportError("$ANTELOPE environment variable not set")
                from antelope.datascope import closing,\
                                                dbopen,\
                                                dbTABLE_IS_VIEW
                dbptr = dbopen(kwargs['database_path'], 'r')
            elif 'database_pointer' in kwargs and\
                    isinstance(kwargs['database_pointer'], Dbptr):
                dbptr = dbopen(kwargs['database_path'], 'r')
            else:
                raise ArgumentError("__init__() expected either "\
                        "'database_path' or 'database_pointer' keyword "\
                        "argument")
            dbptr = dbptr.lookup(table='wfdisc')
            if isinstance(kwargs['starttime'], float) or isinstance(kwargs['starttime'], int):
                kwargs['starttime'] = UTCDateTime(kwargs['starttime'])
            if isinstance(kwargs['endtime'], float) or isinstance(kwargs['endtime'], int):
                kwargs['endtime'] = UTCDateTime(kwargs['endtime'])
            dbptr = dbptr.subset("sta =~ /{:s}/ && chan =~ /{:s}/ && "\
                    "endtime > _{:s}_ && time < _{:s}_".format(kwargs['station'],
                                                               kwargs['channel'],
                                                               kwargs['starttime'],
                                                               kwargs['endtime']))
            if dbptr.record_count == 0:
                raise InitializationError("__init__() found no data for "\
                        "{:s}:{:s} {:s}-{:s}".format(kwargs['station'],
                                                     kwargs['channel'],
                                                     kwargs['starttime'],
                                                     kwargs['endtime']))
            st = Stream()
            for record in dbptr.iter_record():
                st += read(record.filename()[1],
                           starttime=kwargs['starttime'],
                           endtime=kwargs['endtime'])[0]
            st.merge()
            tr = st[0]
            self.stats = tr.stats
            self.data = tr.data
