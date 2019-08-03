import numpy as np
import os
import pandas as pd
import pickle
import pkg_resources
from . import schema as _schema

def read_special(path, schema="hypoinverse2000", tables=None):
    """
    Read database tables into a Pandas DataFrame. This function
    is for reading formats that don't lend themselves to more
    general parsing routines. Data downloaded from SCEDC in the
    hypoinverse2000 phase format is motivating this; it does not
    lend itself to the more general fixed-width format parsing
    function because it contains both origin and arrival rows that
    need to be parsed simultaneously.

    Positional arguments
    ====================
    path ::str:: path to database

    Keyword arguments
    =================
    schema ::str:: schema handle
    tables ::iterable:: a list of table names to read

    Returns
    =======
    A dictionary with table names as keys and pandas.DataFrames as
    values.
    """

    if schema == "hypoinverse2000":
        return(_read_hypoinverse2000(path))
    else:
        raise(NotImplementedError("schema not recognized: %s" % schema))

def _index_rows(fname):
    """
    Return the total number of lines and indices of origin
    rows in input file.

    This is a utility function for parsing hypoinverse2000
    phase format data.
    """
    with open(fname) as inf:
        data = inf.read().rstrip("\n").split("\n")
    nrows = len(data)
    # The variable lengths (164, 179) of origin rows is to account for NCEDC
    # format data which is slightly different than SCEDC data.
    return (
        nrows,
        np.array([i for i in range(len(data)) if len(data[i]) in (164, 179)]),
        np.array([i for i in range(len(data)) if len(data[i]) == 120])
    )

def _read_hypoinverse2000(path):
    schema_data = _schema.get_schema("hypoinverse2000")
    nrows, origin_rows, arrival_rows = _index_rows(path)
    db = {}
    db["origin"] = pd.read_fwf(
        path,
        widths=[
            schema_data["Attributes"][field]["width"]
            for field in schema_data["Relations"]["origin"]
        ],
        names=schema_data["Relations"]["origin"],
        skiprows=[i for i in range(nrows) if i not in origin_rows],
        header=None
    )
    db["arrival"] = pd.read_fwf(
        path,
        widths=[
            schema_data["Attributes"][field]["width"]
            for field in schema_data["Relations"]["arrival"]
        ],
        names=schema_data["Relations"]["arrival"],
        skiprows=[i for i in range(nrows) if i not in arrival_rows],
        header=None
    )
    start = 0
    for iorigin in range(len(origin_rows)-1):
        stop = start + len(
            arrival_rows[
                 (arrival_rows > origin_rows[iorigin])
                &(arrival_rows < origin_rows[iorigin+1])
            ]
        )
        db['arrival'].loc[start: start+nrows, 'evid'] = db['origin'].loc[iorigin, 'evid']
        start = stop
    for table in db:
        db[table] = db[table].fillna(
            value={
                field: schema_data["Attributes"][field]["null"]
                for field in db[table].columns
            }
        )
        db[table] = db[table].astype(
           {
               field: schema_data["Attributes"][field]["dtype"]
               for field in db[table].columns
           }
        )
        for field in db[table].columns:
            if "const" in schema_data["Attributes"][field]:
                db[table][field] = db[table][field] \
                    * schema_data["Attributes"][field]["const"]
    db["arrival"] = db["arrival"].drop(columns=["blank1", "blank2", "blank3"])
    return (db)
