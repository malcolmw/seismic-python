'''
A container class for database schema definitions.
'''
from os.path import isfile
from seispy.core.exceptions import InitializationError
_lead_tokens = ('(', '{', '"', "'", 'Attribute', 'Detail', 'Relation', 'Schema')
_token_conjugates = {'(': ')',
                     '{': '}',
                     '"': '"',
                     "'": "'",
                     'Attribute': ';',
                     'Detail': ';',
                     'Relation': ';',
                     'Schema': ';'}

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


class Attribute:
    def __init__(self, *args, **kwargs):
        pass

class AttributeParseError:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Schema:
    def __init__(self, path):
        self.token_parser = TokenParser(path)
        self.parse_header()

    def parse_attribute(self):
        while True:
            line = self.infile.readline().strip()
            if line == '': continue
            spec, value = line.split()
            token, pos, conj = find_token(value)
            if pos == None:
                raise AttributeParseError("no lead token found while parsing "\
                        "Attribute")
            if conj == None:
                pass
            value = value[pos + 1:]
            token, pos, conj = find_token(value, ttype=conj)

    def parse_header(self):
        if not token_parser.get_chunk() == 'Schema':
            raise Exception("Error code 1000")
        schema_header = TokenParser(token_parser.get_chunk())
        self.schema = schema_header.get_chunk()
        if not schema_header.get_chunk() == 'Description':
            raise Exception("Error code 1001")
        desc_block = schema_header.get_chunk()
        if not schema_header.get_chunk() == 'Detail':
            raise Exception("Error code 1002")
        det_block = schema_header.get_chunk()

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
        self.token = None
        self.chunk = ''

    def get_chunk(self):
        self.chunk = self.next()
        if self.chunk == '':
            print "get_chunk(1) ==> None"
            return None
        elif self.chunk == None:
            print "get_chunk(2) ==> None"
            return None
        elif not self.token == '}'  and not self.token == ';'\
                and (self.chunk == '\n' or self.chunk == '\t'):
            while self.chunk == '\n' or self.chunk == '\t':
                print "get_chunk(3) ==> while..."
                self.chunk = self.next()
        #Need to check the value of self.token here...
        elif self.chunk == ' ' or self.chunk == '\t' or self.chunk in _lead_tokens:
            while self.chunk == ' ' or self.chunk == '\t' or self.chunk in _lead_tokens:
                print "get_chunk(4) ==> while... {:s}".format(self.chunk)
                self.chunk = self.next()
                if self.chunk in _lead_tokens:
                    print "get_chunk(4) ==> break... {:s}".format(self.chunk)
                    break
        if self.chunk in _lead_tokens:
            self.token = _token_conjugates[self.chunk]
            print "get_chunk(5) ==> {:s}".format(self.chunk)
            return self.chunk
        while True:
            c = self.next()
            if c == None:
                print "get_chunk(6) ==> {:s}".format(self.chunk)
                return self.chunk
            self.chunk += c
            if self.token:
                if c == self.token:
                    self.token = None
                    print "get_chunk(7) ==> {:s}".format(self.chunk[:-1].rstrip().lstrip())
                    return self.chunk[:-1].rstrip().lstrip()
            else:
                if c == '\n':
                    self.token = None
                    self.chunk += c
                    print "get_chunk(8) ==> {:s}".format(self.chunk.rstrip().lstrip())
                    return self.chunk.rstrip().lstrip()
                elif c in _lead_tokens:
                    self.token = _token_conjugates[c]
                    print "get_chunk(9) ==> {:s}".format(self.chunk.rstrip().lstrip())
                    return self.chunk[:-1].rstrip().lstrip()
                elif self.chunk in _lead_tokens:
                    print "get_chunk(10) ==> {:s}".format(self.chunk.rstrip().lstrip())
                    self.token = _token_conjugates[self.chunk]
                    return self.chunk.rstrip().lstrip()

    def next(self):
        if self.type == file:
            c = self.stream.read(1)
            if c == '':
                return None
            else:
                if c == '':
                    return None
                return c
        else:
            if len(self.stream) == 0:
                return None
            else:
                c = self.stream[0]
                self.stream = self.stream[1:]
                return c
