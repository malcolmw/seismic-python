import numpy as np
import os
import pandas as pd
import seismic_pandas as _sp

IO_FUNCS = {"csv": lambda *args, **kwargs: {"catalog": pd.read_csv(*args, **kwargs)},
            # "empty": lambda *args, **kwargs: {},
            "fwf": _sp.io.fixed_width.read_fwf,
            "special": _sp.io.special.read_special}

class Catalog(object):
    def __init__(self, *args, **kwargs):
        """
        This is a wrapper around IO functions that are defined in
        seismic_pandas.io and registered in IO_FUNCS.
        
        Positional arguments
        ====================
        *args       ::tuple:: passed directly to underlying IO function.
        
        Keyword arguments
        =================
        fmt         ::str:: data format - ("csv", fwf").
        schema      ::str:: data schema - ("css3.0", "scsn1.0", "hys1.0", "growclust1.0").
        **kwargs    ::dict:: passed directly to underlying IO function.
        """
        self._data = None
        self._fmt = kwargs["fmt"].lower() if "fmt" in kwargs else None
        self._schema = kwargs["schema"].lower() if "schema" in kwargs else None
        if len(args) == 0:
            return
        if "fmt" not in kwargs:
            raise(ValueError("caller must provide kwarg: fmt"))
        if "schema" not in kwargs and self._fmt != "csv":
            raise(ValueError("caller must provide kwarg: schema"))
        if self._fmt not in IO_FUNCS:
            raise(NotImplementedError("unrecognized format: %s" % self._fmt))
        del(kwargs["fmt"])
        self._data = IO_FUNCS[self._fmt](*args, **kwargs)

    def __getitem__(self, key):
        """
        Support data access via indexing.
        """
        if key not in self._data:
            raise(KeyError)
        return(self._data[key])

    def __setitem__(self, key, value):
        """
        Support data assignment via indexing.
        """
        if self._data is None:
            self._data = {key: value}
        else:
            self._data[key] = value

    def append(self, *args, **kwargs):
        """
        Append catalog data to existing Catalog instance.
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
        """
        Save a catalog using pandas.HDFStore.
        """
        if os.path.exists(outfile):
            raise(IOError("file/directory already exists:", outfile))
        with pd.HDFStore(outfile, "w") as store:
            store["meta"] = pd.DataFrame().from_dict({"fmt": [self._fmt],
                                                      "schema": [self._schema]})
            for table in self._data.keys():
                store[table] = self[table]
        
    def prefor_only(self):
        """
        This is necessary to account for the fact that Antelope
        allow many origins for a single event, and a preferred
        origin flagged for each event.
        This will return a new catalog with only the preferred
        origins.
        """
        if self._schema != "css3.0":
            raise(NotImplementedError("you'll have to give me instructions"))
        df = self["origin"].merge(self["event"][["evid", "prefor"]])
        df = df[df["orid"] == df["prefor"]][df.columns.drop("prefor")]
        cat = Catalog(fmt="empty")
        cat["origin"] = df
        return(cat)

    def write(self, path):
        _sp.io.fixed_width.write_fwf(self, path, self._schema)


def load(infile):
    """
    This should load a catalog as a dictionary pandas.DataFrames
    using pandas.HDFStore.
    """
    with pd.HDFStore(infile, "r") as store:
        fmt, schema = store["meta"].iloc[0]
        cat = _sp.catalog.Catalog(fmt=fmt, schema=schema)
        cat._data = {}
        for key in store:
            key = key.lstrip("/")
            if key == "meta":
                continue
            cat._data[key] = store[key]
    return(cat)
