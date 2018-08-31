#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 11:19:41 2018

@author: malcolcw
"""

import os
import pandas as pd

def read_h5(*args, **kwargs):
    r"""Load a catalog from HDF5 using pandas.HDFStore.
    """
    with pd.HDFStore(kwargs["path"], "r") as store:
        fmt, schema = store["meta"].iloc[0]
        data = {}
        for key in store:
            key = key.lstrip("/")
            if key == "meta":
                continue
            data[key] = store[key]
    return(data)

def write_h5(data, path, schema, overwrite=False):
    r"""Save catalog in HDF5 using pandas.HDFStore.
    """
    if os.path.exists(path) and overwrite is False:
        raise(IOError("file/directory already exists:", path))
    with pd.HDFStore(path, "w") as store:
        store["meta"] = pd.DataFrame().from_dict({"fmt": ["hdf5"],
                                                  "schema": [schema]})
        for table in data.keys():
            store[table] = data[table]