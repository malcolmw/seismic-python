'''
A container class for database schema definitions.
'''
from inspect import getmembers
from os.path import isfile
from seispy.core.exceptions import InitializationError
_lead_tokens = ('(', '{', '"')
_token_conjugates = {'(': ')',
                     '{': '}',
                     '"': '"',
                     "'": "'"}
_attribute_dtypes = ('String', 'Integer', 'Real')

def find_token(string, ttype=None):
    '''
    Return the position and conjugate of the first instance of a token.

    Specifying keyword 'ttype' will restrict search to tokens equal to
    the value of ttype.
    '''
    if ttype and ttype not in _token_conjugates:
        raise ValueError("invalid ttype")
    if ttype and not isinstance(ttype, str):
        raise TypeError("keyword argument 'ttype' must be type str")
    for i in range(len(string)):
        char = string[i]
        if ttype:
            if char == ttype:
                return char, i, _token_conjugates[ttype]
        else:
            if char in _token_conjugates:
                return char, i, _token_conjugates[char]
    return None, None

class DatabaseElement:
    def __init__(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        keys = []
        s = ''
        for key, value in getmembers(self):
            if len(key) > 2 and key[:2] == '__':
                continue
            if hasattr(value, '__call__'):
                continue
            keys += [key]
        s = ''
        width = max([len(k) for k in keys])
        for key in keys:
            s += "{:>{width}}:".format(key, width=width)
            s += "\t{}\n".format(getattr(self, key))
        return s

class Attribute(DatabaseElement):
    pass

class AttributeParseError:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Relation(DatabaseElement):
    def __str__(self):
        s = self.name + "\n"
        s += "-" * len(self.name)
        width = max([len(attr) for attr in self.attributes])
        for attr in self.attributes:
            s += "{:>{width}}\n".format(attr, width=width)
        return s

class Schema:
    def __init__(self, path):
        self.attributes = {}
        self.relations = {}
        self.token_parser = TokenParser(path)
        self.parse_header()
        self.parse_body()

    def __str__(self):
        s = ''
        for relation in self.relations:
            s += "{}\n".format(self.relations[relation])
        return s

    def parse_body(self):
        tp = self.token_parser
        block = tp.get_block()
        while tp.get_block():
            tp.get_field()
            #print tp.get_key(), tp.get_value()
            if tp.get_key() == 'Attribute':
                print "self.parse_attribute()"
                self.parse_attribute()
            elif tp.get_key() == 'Relation':
                print "self.parse_relation()"
                self.parse_relation()
            else:
                raise Exception("Error code 3000: unrecognized specifier "\
                        "{:s}".format(tp.get_key()))

    def parse_attribute(self):
        tp = self.token_parser
        kwargs = {}
        name = tp.get_value()
        kwargs['name'] = name
        while tp.get_field():
            key = tp.get_key()
            if name == 'net':
                print name, key, tp.get_value()
            if key in _attribute_dtypes:
                kwargs['dtype'] = key
                kwargs['width'] = tp.get_value()
            else:
                kwargs[key] = tp.get_value()
        self.attributes[name] = Attribute(**kwargs)

    def parse_relation(self):
        tp = self.token_parser
        kwargs = {}
        name = tp.get_value()
        kwargs['name'] = name
        while tp.get_field():
            kwargs[tp.get_key()] = tp.get_value()
        self.relations[name] = Relation(**kwargs)

    def parse_header(self):
        tp = self.token_parser
        tp.get_block()
        tp.get_field()
        if tp.get_key() != 'Schema':
            raise Exception("Error code 1000")
        self.schema = tp.get_value()
        field = tp.get_field()
        if tp.get_key() != 'Description':
            raise Exception("Error code 1001")
        self.description= tp.get_value()
        tp.get_field()
        if tp.get_key() != 'Detail':
            raise Exception("Error code 1002")
        self.detail = tp.get_value()
        tp.get_field()
        if tp.get_key() != 'Timedate':
            raise Exception("Error code 1003")
        self.timedate = tp.get_value()

class TokenParser:
    def __init__(self, *args):
        if isfile(args[0]):
            self.type = file
            self.stream = open(args[0], 'r')
        elif isinstance(args[0], str):
            self.type = str
            self.stream = args[0]
        else:
            raise InitializationError("unrecognized argument type")

    def get_block(self):
        tokens = []
        char = self.next()
        if char == None:
            return None
        self.block = char
        while char != ';' or tokens:
            char = self.next()
            #print "!{}$".format(char)
            if char == None:
                self.block = None
                return None
            if tokens and char == tokens[-1]:
                tokens.pop()
            elif char in _lead_tokens:
                tokens += [_token_conjugates[char]]
            self.block += char
        self.block_cursor = 0
        return self.block

    def get_field(self):
        self.field = ''
        tokens = []
        while self.block_cursor < len(self.block):
            char = self.block[self.block_cursor]
            self.block_cursor += 1
            if tokens and char == tokens[-1]:
                tokens.pop()
            elif char in _lead_tokens:
                tokens += [_token_conjugates[char]]
            if not tokens and char == '\n':
                if self.field == '':
                    self.get_field()
                return self.field
            self.field += char
        self.field = None
        return None

    def get_key(self):
        if self.field == None:
            return None
        return self.field.strip().split()[0]

    def get_value(self):
        if self.field == None:
            return None
        field = self.field.lstrip()
        i = 0
        while field[i] != ' ':
            i += 1
        val = field[i:].strip()
        if val[0] in _lead_tokens and val[-1] == _token_conjugates[val[0]]:
            val = val[1:-1]
        return val.strip()

    def next(self):
        if self.type == file:
            c = self.stream.read(1)
            if c == '':
                return None
            else:
                return c
        else:
            if len(self.stream) == 0:
                return None
            else:
                c = self.stream[0]
                self.stream = self.stream[1:]
                return c
