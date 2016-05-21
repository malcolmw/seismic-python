'''
A class to enable database manipulation and querying.
'''
from os.path import isfile
from seispy.util.schema import Schema

class Database:
    def __init__(self, database_path):
        if not isinstance(database_path, str):
            raise TypeError("exected a string argument, got "\
                    "{:s}".format(type(database_path)))
        if not isfile(database_path):
            raise InitializationError("{:s} does not "\
                    "exist".format(database_path))
        self.descriptor_file = open(database_path, 'r')
        while True:
            line = self.descriptor_file.readline()
            if line.split()[0] == 'schema':
                self.schema = line.split()[1]
                break
            elif line.split()[0] == 'dbpath':
                self._set_dbpath(line.split()[1])
        self.schema = Schema("/Users/mcwhite/src/Seispy/data/"\
                "{:s}".format(self.schema))
        self.table = None
        self.field = None
        self.record = None

    def __str__(self):
        s = ''
        for element in ('table', 'field', 'record'):
            s += "{:6}: {:s}\n".format(element, getattr(self, element))
        return s

    def _set_dbpath(self, dbpath):
        dbp = []
        for path in dbpath.split(':'):
            dbp += [path[:path.find('{')] + path[path.find('{') + 1:path.find('}')]]
        self._dbpath = tuple(dbp)


    def lookup(self, **kwargs):
        for key in kwargs:
            if key not in ('table', 'field', 'record'):
                #raise ArgumentError("unrecognized keyword {:s}".format(key))
                raise Exception("unrecognized keyword {:s}".format(key))
        if self.table == None and 'table' not in kwargs:
            raise Exception("lookup must specify a table")
        for key in ('table', 'field', 'record'):
            if key not in kwargs:
                continue
            elif key == 'table':
                if kwargs[key] not in self.schema.relations:
                    raise Exception("cannot lookup table {:s}".format(kwargs[key]))
                self.table = self.schema.relations[kwargs[key]]
            elif key == 'field':
                raise Exception("field lookup not implemented")
            elif key == 'record':
                raise Exception("record lookup not implemented")

    def get(self, *args):
        pass
