r"""
.. codeauthor:: Malcolm White

.. autoclass:: Catalog
   :members:
"""
import os
import pandas as pd
from . import catalog as _catalog
from . import io as _io

IO_FUNCS = {"read": {"fwf": _io.fixed_width.read_fwf,
                     "hdf5": _io.h5.read_h5,
                     "special": _io.special.read_special,
                     "table": _io.table.read_table},
            "write": {"fwf": _io.fixed_width.write_fwf,
                      "hdf5": _io.h5.write_h5}
            }


class Catalog(object):
    r"""An earthquake catalog.

    :param str fmt: Data format - ("csv", fwf").
    :param str schema: Data schema - ("css3.0", "scsn1.0", "hys1.0",
                       "growclust1.0").
    :param dict kwargs: Passed directly to underlying IO function.

    Known bugs:
    - When reading from an HDF5 format file, the resulting catalog's
    schema attribute will
    not be properly set unless done explicitly using the schema keyword
    argument when
    instantiating the object.
    """

    def __init__(self, path=None, fmt="fwf", schema="css3.0", **kwargs):
        self._data = None
        self._fmt = fmt.lower()
        self._schema = schema.lower()
        if path is None:
            return
        assert self._fmt in IO_FUNCS["read"]
        self._data = IO_FUNCS["read"][self._fmt](path=path, 
                                                 schema=schema, 
                                                 **kwargs)

    def __getitem__(self, key):
        r"""Support data access via indexing.
        """
        if key not in self._data:
            raise(KeyError)
        return(self._data[key])

    def __setitem__(self, key, value):
        r"""Support data assignment via indexing.
        """
        if self._data is None:
            self._data = {key: value}
        else:
            self._data[key] = value

    def add_null(self, tables):
        r"""Add null row to table(s).
        
        :param str,list tables: Table or list of tables to add null row(s) to.
        """
        tables = (tables,) if isinstance(tables, str) else tables
        for table in tables:
            null = _io.schema.get_null(self._schema, table)
            self[table] = self[table].append(null, ignore_index=True)
    
    def add_row(self, table, data):
        r"""Add a new row of data to table.
        
        :param str table: Table to add data to.
        :param dict data: Data to append.
        """
        idx = len(self[table])
        self.add_null(table)
        self[table].loc[idx, data.keys()] = [data[key] for key in data.keys()]

    def append(self, *args, **kwargs):
        r"""Append catalog data to existing Catalog instance.
        """
        if self._fmt is None and "fmt" not in kwargs:
            raise(ValueError("caller must provide kwarg: fmt"))
        if self._schema is None and "schema" not in kwargs:
            raise(ValueError("caller must provide kwarg: schema"))
        if self._schema is None:
            self._schema = kwargs["schema"]
        elif "schema" in kwargs and self._schema != kwargs["schema"].lower():
            raise(ValueError("kwarg['schema'] != self._schema"))

        fmt = kwargs["fmt"]
        del(kwargs["fmt"])
        data = IO_FUNCS["read"][fmt](*args, **kwargs)

        if self._data is None:
            self._data = {}
        for key in data:
            if key not in self._data:
                self._data[key] = data[key]
            else:
                self._data[key] = pd.concat([self._data[key], data[key]],
                                            ignore_index=True
                                           ).drop_duplicates()

    def save(self, outfile):
        r"""Save catalog in HDF5 using pandas.HDFStore.
        """
        if os.path.exists(outfile):
            raise(IOError("file/directory already exists:", outfile))
        with pd.HDFStore(outfile, "w") as store:
            store["meta"] = pd.DataFrame().from_dict({"fmt": [self._fmt],
                                                      "schema": [self._schema]})
            for table in self._data.keys():
                store[table] = self[table]
    
    def write(self, path, tables=None, fmt=None, overwrite=False):
        r"""Output as formatted text files.
        
        :param str path: Output path.
        :param list tables: List of tables to write.
        :param str fmt: Output format ("fwf", "hdf5", ...)
        """
        tables = self._data.keys() if tables is None \
            else [table for table in tables if table in self._data.keys()]
        data = {table: self[table] for table in tables if len(self[table]) > 0}
        if fmt == None:
            fmt = self._fmt
        IO_FUNCS["write"][fmt](data, path, self._schema, overwrite=overwrite)

def load(infile):
    r"""Load a catalog from HDF5 using pandas.HDFStore.
    """
    with pd.HDFStore(infile, "r") as store:
        fmt, schema = store["meta"].iloc[0]
        cat = _catalog.Catalog(fmt=fmt, schema=schema)
        cat._data = {}
        for key in store:
            key = key.lstrip("/")
            if key == "meta":
                continue
            cat._data[key] = store[key]
    return(cat)