r"""
.. codeauthor:: Malcolm White

.. autoclass:: Catalog
   :members:
"""
import os
import pandas as pd
from . import catalog as _catalog
from . import io as _io

IO_FUNCS = {"csv": lambda *args, **kwargs: {"catalog": pd.read_csv(*args, **kwargs)},
            "fwf": _io.fixed_width.read_fwf,
            "special": _io.special.read_special}

class Catalog(object):
    r"""An earthquake catalog.

    fmt         ::str:: data format - ("csv", fwf").
    schema      ::str:: data schema - ("css3.0", "scsn1.0", "hys1.0", "growclust1.0").
    **kwargs    ::dict:: passed directly to underlying IO function.
    """
    def __init__(self, path=None, fmt="fwf", schema="css3.0", **kwargs):
        self._data = None
        self._fmt = fmt.lower()
        self._schema = schema.lower()
        assert self._fmt in IO_FUNCS
        self._data = IO_FUNCS[self._fmt](path=path, schema=schema, **kwargs)

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

    def append(self, *args, **kwargs):
        r"""Append catalog data to existing Catalog instance.
        """
        if self._fmt is None and "fmt" not in kwargs:
            raise(ValueError("caller must provide kwarg: fmt"))
        if self._schema is None and "schema" not in kwargs:
            raise(ValueError("caller must provide kwarg: schema"))
        if self._fmt is None:
            self._fmt = kwargs["fmt"]
        elif "fmt" in kwargs:
            if self._fmt != kwargs["fmt"].lower():
                raise(ValueError("kwarg['fmt'] != self._fmt"))
        try:
            del(kwargs["fmt"])
        except KeyError:
            pass
        if self._schema is None:
            self._schema = kwargs["schema"]
        elif "schema" in kwargs and self._schema != kwargs["schema"].lower():
            raise(ValueError("kwarg['schema'] != self._schema"))

        data = IO_FUNCS[self._fmt](*args, **kwargs)

        if self._data is None:
            self._data = {}
        for key in data:
            if key not in self._data:
                self._data[key] = data[key]
            else:
                self._data[key] = pd.concat([self._data[key], data[key]],
                                            ignore_index=True)

    def save(self, outfile):
        r"""Save a catalog using pandas.HDFStore.
        """
        if os.path.exists(outfile):
            raise(IOError("file/directory already exists:", outfile))
        with pd.HDFStore(outfile, "w") as store:
            store["meta"] = pd.DataFrame().from_dict({"fmt": [self._fmt],
                                                      "schema": [self._schema]})
            for table in self._data.keys():
                store[table] = self[table]

def load(infile):
    r"""Load a catalog using pandas.HDFStore.
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
