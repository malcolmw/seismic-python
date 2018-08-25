import os
import pandas as pd

from . import schema as _schema

def read_fwf(path=None, schema="css3.0", tables=None):
    r"""Read fixed-width-format database tables into a DataFrame.

    :param str path: Path to database.
    :param str schema: Schema identifier.
    :param list tables: A list of table populate.
    :return: A dict with table names for keys and pandas.DataFrames as
             values.
    :rtype: dict
    """
    schema_name = schema
    # Get the schema.
    schema = _schema.get_schema(schema)
    # Build the list of tables to populate.
    tables = [table for table in tables
                    if table in schema["Relations"].keys()]\
             if tables is not None\
             else schema["Relations"].keys()
    # If no path is provided, populate tables with null values.
    if path is None:
        data = {table: _schema.get_null(schema_name, table) 
                for table in tables}
        return(data)
    # Read data files and build tables.
    data = {table: pd.read_fwf("%s.%s" % (path, table),
                             names=schema["Relations"][table],
                             widths=[schema["Attributes"][field]["width"]+1
                                     for field in schema["Relations"][table]],
                             comment=schema["comment"] if "comment" in schema
                                                       else None)
         if os.path.isfile("%s.%s" % (path, table))
         else _schema.get_null(schema_name, table)
         for table in tables}
    # Coerce dtype of every field.
    for table in tables:
        for field in schema["Relations"][table]:
            data[table][field] = data[table][field].astype(schema["Attributes"][field]["dtype"])
    return(data)

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
