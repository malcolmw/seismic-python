import os
import pandas as pd

from . import schema as _schema


def read_table(path=None, schema="css3.0", tables=None):
    r"""Read white-space delimieted database tables into a DataFrame.

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
        data = {table: _schema.get_empty(schema_name, table)
                for table in tables}
        return(data)
    # Read data files and build tables.
    comment = schema["comment"] if "comment" in schema else None
    data = {table: pd.read_table("%s.%s" % (path, table),
                                 names=schema["Relations"][table],
                                 delim_whitespace=True,
                                 comment=comment)
            if os.path.isfile("%s.%s" % (path, table))
            else _schema.get_empty(schema_name, table)
            for table in tables}
    # Coerce dtype of every field.
    for table in tables:
        for field in schema["Relations"][table]:
            data[table][field] = data[table][field].astype(
                schema["Attributes"][field]["dtype"])
    return(data)
