import os
import pandas as pd
import pickle
import pkg_resources

from . import schema as _schema

def read_fwf(path, schema="css3.0", tables=None):
    """
    Read Antelope format database tables into a Pandas DataFrame.

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
    schema_data = _schema.get_schema(schema)

    tables = [table for table in tables
                    if os.path.isfile("%s.%s" % (path, table))]\
             if tables is not None\
             else [table for table in schema_data["Relations"].keys()
                         if os.path.isfile("%s.%s" % (path, table))]
    for table in tables:
        if table not in schema_data["Relations"]:
            raise(ValueError("table name not recognized: %s" % table))

    db = {table: pd.read_fwf("%s.%s" % (path, table),
                             names=schema_data["Relations"][table],
                             widths=[schema_data["Attributes"][field]["width"]+1
                                     for field in schema_data["Relations"][table]],
                             comment=schema_data["comment"] if "comment" in schema_data
                                                            else None)
         for table in tables}
    for table in tables:
        for field in schema_data["Relations"][table]:
            db[table][field] = db[table][field].astype(schema_data["Attributes"][field]["dtype"])
    return(db)

def write_fwf(cat, path, schema):
    for table in cat._data:
        if os.path.isfile("%s.%s" % (path, table)):
            raise(IOError("file already exists: %s.%s" % (path, table)))

    schema_data = _schema.get_schema(schema)

    for table in cat._data:
        fields = schema_data["Relations"][table]
        fmt = " ".join([schema_data["Attributes"][field]["format"]
                        for field in schema_data["Relations"][table]])
        with open("%s.%s" % (path, table), "w") as outf:
            outf.write(
                "\n".join([fmt % tuple(row) for _, row in cat[table][fields].iterrows()]) + "\n"
                      )
