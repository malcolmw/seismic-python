'''
A container class for database schema definitions.
'''
from inspect import getmembers
from math import floor
from os import mkdir
from os.path import isfile, isdir
from shutil import rmtree

from seispy import _datadir
from seispy.core.exceptions import InitializationError
from seispy.util.time import verify_time
_lead_tokens = ('(', '{', '"')
_token_conjugates = {'(': ')',
                     '{': '}',
                     '"': '"',
                     "'": "'"}
_attribute_dtypes = {'Dbptr': None,
                     'Integer': int,
                     'Real': float,
                     'String': str,
                     'Time': float,
                     'Transient': None,
                     'YearDay': verify_time}

#base class
class SchemaElement:
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

class Attribute(SchemaElement):
    def sphinx_documentation_block(self, schema="NOSCHEMA", ref_sufx="_attributes"):
        block = ".. _%s-%s%s:\n\n" % (schema, self.name, ref_sufx)
        if hasattr(self, 'description'):
            title = "**%s** -- %s" % (self.name, self.description)
        else:
            title = "**%s**" % self.name
        block += title + "\n"
        block += "-" * len(title) + "\n\n"
        if hasattr(self, 'detail'):
            block += self.detail + "\n\n"
        if hasattr(self, 'width'):
            block += "* **Field width:** %s\n" % self.width
        if hasattr(self, 'format'):
            block += "* **Format:** %s\n" % self.format
        if hasattr(self, 'null'):
            block += "* **Null:** %s\n" % self.null
        if hasattr(self, 'units'):
            block += "* **Units:** %s\n" % self.units
        if hasattr(self, 'range'):
            block += "* **Range:** %s\n" % self.range
        return block


class AttributeParseError:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Relation(SchemaElement):
    def __str__(self):
        line_width = 76
        attr_width = max([len(attr) for attr in self.attributes])
        s = "=" * (line_width + 4) + "\n"
        s += "= {:^{width}} =".format(self.name, width=line_width) + "\n"
        s += "= {:^{width}} =".format("-" * len(self.name), width=line_width) + "\n"
        line = '|'
        for attr in self.attributes:
            if len(line) + attr_width + 1 > line_width:
                s += "= {:^{width}} =".format(line, width=line_width) + "\n"
                line = '|'
            line += "{:^{width}}|".format(attr, width=attr_width)
        s += "= {:^{width}} =".format(line, width=line_width) + "\n"
        s += "=" * (line_width + 4) + "\n"
        return s

    def sphinx_documentation_block(self,
                                   schema="NOSCHEMA",
                                   ref_sufx="_relations",
                                   attr_ref_sufx="_attributes"):
        block = ".. _%s-%s%s:\n\n" % (schema, self.name, ref_sufx)
        if hasattr(self, 'description'):
            title = "**%s** -- %s" % (self.name, self.description)
        else:
            title = "**%s**" % self.name
        block += title + "\n"
        block += "-" * len(title) + "\n\n"
        if hasattr(self, 'detail'):
            block += self.detail + "\n\n"
        if hasattr(self, 'fields'):
            block += "Fields\n^^^^^^\n\n"
            block += draw_table(self.fields,
                                schema=schema) + "\n"
        if hasattr(self, 'primary_keys'):
            block += "Primary Keys\n^^^^^^^^^^^^\n\n"
            block += draw_table(self.primary_keys,
                                schema=schema) + "\n"
        if hasattr(self, 'alternate_keys'):
            block += "Alternate Keys\n^^^^^^^^^^^^^^\n\n"
            block += draw_table(self.alternate_keys,
                                schema=schema) + "\n"
        if hasattr(self, 'foreign_keys'):
            block += "Foreign Keys\n^^^^^^^^^^^^\n\n"
            block += draw_table(self.foreign_keys,
                                schema=schema) + "\n"
        if hasattr(self, 'defines'):
            block += "Defines\n^^^^^^^\n\n"
            block += draw_table(self.defines,
                                schema=schema) + "\n"
        return block


class Schema:
    def __init__(self, *args, **kwargs):
        self.attributes = {}
        self.relations = {}
        if 'path' in kwargs:
            self.token_parser = TokenParser(kwargs['path'])
        elif 'schema' in kwargs:
            print _datadir + kwargs['schema']
            self.token_parser = TokenParser(_datadir + kwargs['schema'])
        else:
            raise InitializationError("specify either 'path' or 'schema' "\
                    "keyword argument")
        self.parse_header()
        self.parse_body()
        self.attributes = sorted([self.attributes[a] for a in self.attributes],
                                 key=sort_key)
        self.relations = sorted([self.relations[r] for r in self.relations],
                                 key=sort_key)

    def __str__(self):
        s = ''
        for relation in self.relations:
            s += "{}\n".format(self.relations[relation])
        return s

    def parse_body(self):
        tp = self.token_parser
        while tp.get_block():
            tp.get_field()
            if tp.get_key() == 'Attribute':
                self.parse_attribute()
            elif tp.get_key() == 'Relation':
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
            if key in _attribute_dtypes:
                kwargs['dtype'] = key.lower()
                kwargs['width'] = tp.get_value()
            elif key == 'Detail':
                lines = tp.get_value().strip('"').splitlines()
                kwargs['detail'] = '\n'.join([line.lstrip() for line in \
                        tp.get_value().strip('"').splitlines()])

            else:
                kwargs[key.lower()] = ' '.join(tp.get_value().strip('"').split())
        self.attributes[name] = Attribute(**kwargs)

    def parse_relation(self):
        tp = self.token_parser
        kwargs = {}
        name = tp.get_value()
        kwargs['name'] = name
        kwargs['transient'] = False
        while tp.get_field():
            key = tp.get_key()
            if key == 'Fields' or\
                    key == 'Primary' or\
                    key == 'Alternate' or\
                    key == 'Foreign' or\
                    key == 'Defines':
                if key == 'Fields':
                    key = 'fields'
                elif key == 'Primary':
                    key = 'primary_keys'
                elif key == 'Alternate':
                    key = 'alternate_keys'
                elif key == 'Foreign':
                    key = 'foreign_keys'
                elif key == 'Defines':
                    key = 'defines'
                kwargs[key] = []
                for attr in tp.get_value().split():
                    if '::' in attr:
                        attr1, attr2 = attr.split('::')
                        kwargs[key] += [(self.attributes[attr1],
                                         self.attributes[attr2])]
                    else:
                        kwargs[key] += [self.attributes[attr]]
                kwargs[key] = sorted(kwargs[key], key=sort_key)
            elif key == 'Transient':
                kwargs['transient'] = True
            else:
                kwargs[tp.get_key().lower()] = ' '.join(tp.get_value().strip('"').split())
        self.relations[name] = Relation(**kwargs)

    def parse_header(self):
        tp = self.token_parser
        tp.get_block()
        while tp.get_field():
            if tp.get_key() == 'Schema':
                self.schema = tp.get_value().strip('"')
            if tp.get_key() == 'Description':
                self.description= tp.get_value().strip('"')
            if tp.get_key() == 'Detail':
                self.detail = tp.get_value().strip('"')
            if tp.get_key() == 'Timedate':
                self.timedate = tp.get_value()

    def write_sphinx_docs(self, output_dir):
        if not isdir(output_dir):
            mkdir(output_dir)
        subdir = "%s/%s" % (output_dir, self.schema)
        if isdir(subdir):
            rmtree(subdir)
        mkdir(subdir)
        mkdir("%s/attributes" % subdir)
        mkdir("%s/relations" % subdir)
        attr_indices, rel_indices = [], []
        for attr in self.attributes:
            if attr.name[0].upper() not in attr_indices:
                attr_indices += [attr.name[0].upper()]
        for rel in self.relations:
            if rel.name[0].upper() not in rel_indices:
                rel_indices += [rel.name[0].upper()]
        self.write_schema_index(subdir,
                                attr_indices=attr_indices,
                                rel_indices=rel_indices)
        self.write_schema_element_index(subdir,
                                        elements='attributes',
                                        indices=attr_indices)
        self.write_schema_element_index(subdir,
                                        elements='relations',
                                        indices=rel_indices)
        for char in attr_indices:
            self.write_schema_element_index(subdir,
                                            key=char,
                                            elements='attributes')
        for char in rel_indices:
            self.write_schema_element_index(subdir,
                                            key=char,
                                            elements='relations')
        attr_indices = self.write_schema_elements(subdir, elements='attributes')
        rel_indices = self.write_schema_elements(subdir, elements='relations')

    def write_schema_index(self, subdir, attr_indices=None, rel_indices=None):
        fout = open("%s/%s_index.rst" % (subdir, self.schema), 'w')
        fout.write(".. _%s_schema_index:\n\n" % self.schema)
        if hasattr(self, 'description'):
            title = "**%s** -- %s" % (self.schema, self.description)
        else:
            title = "**%s**" % self.schema
        fout.write("%s\n" % title + "=" * len(title) + "\n\n")
        fout.write(".. toctree::\n")
        fout.write("   :hidden:\n\n")
        fout.write("   attributes/attributes_index_all\n")
        fout.write("   relations/relations_index_all\n\n")
        if attr_indices:
            fout.write("Attributes\n----------\n\n")
            index = ""
            for char in attr_indices:
                index += ":ref:`%s <%s_attributes_index_%s>` | " %\
                        (char, self.schema, char)
            index += ":ref:`all <%s_attributes_index_all>`" % self.schema
            fout.write("%s\n\n" % index)
        if rel_indices:
            fout.write("Relations\n---------\n\n")
            index = ""
            for char in rel_indices:
                index += ":ref:`%s <%s_relations_index_%s>` | " %\
                        (char, self.schema, char)
            index += ":ref:`all <%s_relations_index_all>`" % self.schema
            fout.write("%s\n\n" % index)
        if hasattr(self, 'detail'):
            fout.write("Detail\n------\n\n")
            fout.write("%s\n" % self.detail)
        fout.close()

    def write_schema_element_index(self,
                                   subdir,
                                   key='all',
                                   elements=None,
                                   indices=None):
        if key == 'all':
            objs = getattr(self, elements)
        else:
            objs = [obj for obj in getattr(self, elements) if\
                    obj.name[0].upper() == key]
        if len(objs) == 0:
            return
        fout = open("%s/%s/%s_index_%s.rst" % (subdir, elements, elements, key), 'w')
        fout.write(".. _%s_%s_index_%s:\n\n" % (self.schema, elements, key))
        title = "%s%s Index -- **%s**" % (elements[0].upper(), elements[1:], key)
        fout.write("%s\n" % title + "=" * len(title) + "\n\n")
        #fout.write(draw_table(objs,
        #                      schema=self.schema,
        #                      ref_sufx="_%s" % elements))
        fout.write(draw_table(objs, schema=self.schema) + "\n")
        fout.write(".. toctree::\n")
        fout.write("   :hidden:\n\n")
        if key == 'all':
            for char in indices:
                fout.write("   %s_index_%s\n" % (elements, char))
        else:
            for obj in objs:
                fout.write("   %s\n" % obj.name)
        fout.close()

    def write_schema_elements(self, subdir, elements=None):
        for obj in getattr(self, elements):
            fout = open("%s/%s/%s.rst" % (subdir, elements, obj.name), 'w')
            fout.write(obj.sphinx_documentation_block(schema=self.schema,
                                                      ref_sufx="_%s" % elements))


    def write_sphinx_docs_dep(self, output_dir):
        if not isdir(output_dir):
            mkdir(output_dir)
        subdir = "%s/%s" % (output_dir, self.schema)
        if isdir(subdir):
            rmdir(subdir)
        mkdir(subdir)
        outfile = open("%s/%s.rst" % (output_dir, self.schema), 'w')
        outfile.write(".. _top-%s:\n\n" % self.schema)
        header = "**%s** -- %s" % (self.schema, self.description.strip('"'))
        outfile.write(header + "\n")
        outfile.write("=" * len(header) + "\n")
        outfile.write(self.detail + "\n\n")
        outfile.write(".. _Attributes-%s:\n\n" % self.schema)
        outfile.write(draw_table(self.attributes,
                                 header="Attributes",
                                 schema=self.schema,
                                 ref_sufx='A') + "\n\n")
        outfile.write(".. _Relations-%s:\n\n" % self.schema)
        outfile.write(draw_table(self.relations,
                                 header="Relations",
                                 schema=self.schema,
                                 ref_sufx='R') + "\n\n")
        outfile.write("Attributes\n==========\n")
        for attr in self.attributes:
            outfile.write(attr.sphinx_documentation_block(schema=self.schema))
            outfile.write("\n:ref:`[top] <top-%s>` :ref:`[Attributes] "\
                    "<Attributes-%s>` :ref:`[Relations] <Relations-%s>`\n\n" %\
                    (self.schema, self.schema, self.schema))
        outfile.write("Relations\n=========\n")
        for relation in self.relations:
            outfile.write(relation.sphinx_documentation_block(schema=self.schema))
            outfile.write("\n:ref:`[top] <top-%s>` :ref:`[Attributes] "\
                    "<Attributes-%s>` :ref:`[Relations] <Relations-%s>`\n\n" %\
                    (self.schema, self.schema, self.schema))

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

def draw_table(iterator,
               header=None,
               schema="NULLSCHEMA",
               ncol=6):
    if len(iterator) < ncol:
        ncol = len(iterator)
    cell_entries = {}
    for element in iterator:
        if isinstance(element, tuple):
            key = "%s::%s" % (element[0].name, element[1].name)
            #entry = ":doc:`%s </source/schemas/%s/attributes/%s.rst>`::"\
            #        ":doc:`%s </source/schemas/%s/attributes/%s.rst>`" %\
            #        (element[0].name,
            #         schema,
            #         element[0].name,
            #         element[1].name,
            #         schema,
            #         element[1].name)
            entry = ":ref:`%s <%s-%s_attributes>`::"\
                    ":ref:`%s <%s-%s_attributes>`" %\
                    (element[0].name,
                     schema,
                     element[0].name,
                     element[1].name,
                     schema,
                     element[1].name)
        else:
            if isinstance(element, Attribute):
                suffix = "_attributes"
            elif isinstance(element, Relation):
                suffix = "_relations"
            key = element.name
            #entry = ":doc:`%s </source/schemas/%s/%s/%s.rst>`" %\
            #        (element.name, schema, subdir, element.name)
            entry = ":ref:`%s <%s-%s%s>`" %\
                    (element.name, schema, element.name, suffix)
        cell_entries[key] = entry
    colwidth = max([len(cell_entries[key]) for key in cell_entries])
    tblwidth = ncol * (colwidth + 1) + 1
    if header:
        s = "+" + "-" * (tblwidth - 2) + "+\n"
        s += "|%s" % header + " " * (tblwidth - len("|%s" % header) - 1) + "|\n"
        s += ("+" + "=" * colwidth) * ncol + "+\n"
    else:
        s = ("+" + "-" * colwidth) * ncol + "+\n"
    counter = 1
    for key in sorted(cell_entries):
        entry = cell_entries[key]
        s += "|%s" % entry + " " * (colwidth - len(entry))
        if counter % ncol == 0:
            s += "|\n"
            if counter != len(cell_entries):
                s += ("+" + "-" * colwidth) * ncol + "+" + "\n"
        counter += 1
    if len(cell_entries) % ncol != 0:
        for i in range(ncol - (len(cell_entries) % ncol)):
            s += "|" + " " * colwidth
        s += "|\n"
    s += ("+" + "-" * colwidth) * ncol + "+\n"
    return s

def draw_table_dep(iterator,
               header=None,
               schema="NULLSCHEMA",
               ref_sufx="X",
               ncol=6):
    if len(iterator) < ncol:
        ncol = len(iterator)
    colwidth = max([len(element.name) + 8 + len(schema) + len(ref_sufx)\
            if not isinstance(element, tuple)\
            else (len(element[0].name) +\
                  len(element[1].name) +\
                  18 +\
                  2 * (len(schema) + len(ref_sufx))
                 )\
            for element in iterator])
    tblwidth = ncol * (colwidth + 1) + 1
    if header:
        s = "+" + "-" * (tblwidth - 2) + "+\n"
        s += "|%s" % header + " " * (tblwidth - len("|%s" % header) - 1) + "|\n"
        s += ("+" + "=" * colwidth) * ncol + "+\n"
    else:
        s = ("+" + "-" * colwidth) * ncol + "+\n"
    counter = 1
    for element in iterator:
        if not isinstance(element, tuple):
            name = element.name
            s += "|:doc:`%s-%s%s`" % (schema, name, ref_sufx) +\
                    " " * (colwidth - (len(name) +\
                                       8 +\
                                       len(schema) +\
                                       len(ref_sufx)
                                      )
                          )
        else:
            name1, name2 = element[0].name, element[1].name
            s += "|:doc:`%s-%s%s`:::doc:`%s-%s%s`"\
                    % (schema, name1, ref_sufx, schema, name2, ref_sufx)
            s += " " * (colwidth - (len(name1) +\
                                    len(name2) +\
                                    18 +\
                                    2 * (len(schema) + len(ref_sufx))
                                    )
                       )
        if counter % ncol == 0:
            s += "|\n"
            if counter != len(iterator):
                s += ("+" + "-" * colwidth) * ncol + "+" + "\n"
        counter += 1
    if len(iterator) % ncol != 0:
        for i in range(ncol - (len(iterator) % ncol)):
            s += "|" + " " * colwidth
        s += "|\n"
    s += ("+" + "-" * colwidth) * ncol + "+\n"
    return s

def sort_key(obj):
    if isinstance(obj, SchemaElement):
        return obj.name
    elif isinstance(obj, tuple):
        return obj[0].name
