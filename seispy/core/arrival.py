from seispy.core import DbParsable

class Arrival(DbParsable):
    '''
    A container class for phase data.
    '''
    def __init__(self, *args, **kwargs):
        self.attributes = ()
        if len(args) == 1:
            self._parse_Dbptr(args[0])
        else:
            primary_kwargs = ('sta', 'time', 'iphase')
            for kw in primary_kwargs:
                if kw not in kwargs:
                    raise InitializationError("must specify 'sta', 'time', "\
                            "and 'iphase' for Arrival")
            valid_kwargs = ('sta',
                            'time',
                            'iphase',
                            'chan',
                            'deltim',
                            'qual',
                            'arid',
                            'tt_calc',
                            'predarr')
            for kw in valid_kwargs:
                if kw in kwargs:
                    setattr(self, attr, kwargs[kw])
                else:
                    setattr(self, attr, None)
                self.attributes += (attr,)

