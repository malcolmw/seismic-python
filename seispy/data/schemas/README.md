# Defining schemas
Schemas are defined as pickled dictionaries with two mandatory keys: i) *Attributes* and ii) *Relations*. In addition to the mandatory keys, optional keys may be provided to further specify the schema: i) comment

## Attributes
*Attributes* are synonymous with columns or fields, and each *Attribute* entry is itself a a dictionary with four keys: i) dtype, ii) format, iii) null, and iv) width.

- dtype: data type
- format: format string for converting back to flat file
- null: null value
- width: column width

## Relations
*Relations* are synonymous with tables, and each *Relation* entry is an ordered list of *Attributes* belonging to that *Relation*.

### comment
A string delimiting the start of a comment. Everything between a comment delimiter and the next end-of-line character will be ignored by the parser.

## Example
Below is an example of how to define a simple schema with a single table containing six fields.

```python
>>> import pickle
>>> schema =\
    {"Attributes":
        {"algorithm": {"dtype": str, "format": "%-15s", "null": "-", "width": 15},
         "auth": {"dtype": str, "format": "%-15s", "null": "-", "width": 15},
         "commid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "depdp": {"dtype": float, "format": "%9.4f", "null": -999.0, "width": 9},
         "depth": {"dtype": float, "format": "%9.4f", "null": -999.0, "width": 9},
         "dtype": {"dtype": str, "format": "%-1s", "null": "-", "width": 1},
         "etype": {"dtype": str, "format": "%-2s", "null": "-", "width": 2},
         "evid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "grn": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "jdate": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "lat": {"dtype": float, "format": "%9.4f", "null": -999.0, "width": 9},
         "lddate": {"dtype": float, "format": "%17.5f", "null": -9999999999.999, "width": 17},
         "lon": {"dtype": float, "format": "%9.4f", "null": -999.0, "width": 9},
         "mb": {"dtype": float, "format": "%7.2f", "null": -999.0, "width": 7},
         "mbid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "ml": {"dtype": float, "format": "%7.2f", "null": -999.0, "width": 7},
         "mlid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "ms": {"dtype": float, "format": "%7.2f", "null": -999.0, "width": 7},
         "msid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "nass": {"dtype": int, "format": "%4ld", "null": -1, "width": 4},
         "ndef": {"dtype": int, "format": "%4ld", "null": -1, "width": 4},
         "ndp": {"dtype": int, "format": "%4ld", "null": -1, "width": 4},
         "orid": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "review": {"dtype": str, "format": "%-4s", "null": "-", "width": 4},
         "srn": {"dtype": int, "format": "%8ld", "null": -1, "width": 8},
         "time": {"dtype": float, "format": "%17.5f", "null": -9999999999.999, "width": 17}}
    "Relations":
        "origin": ["lat", "lon", "depth", "time", "orid", "evid", "jdate", "nass",
                   "ndef", "ndp", "grn", "srn", "etype", "review", "depdp", "dtype",
                   "mb", "mbid", "ms", "msid", "ml", "mlid", "algorithm", "auth",
                   "commid", "lddate"]
>>> with open("data/schemas/myschema.1.0.pkl", "wb") as outf:
>>>     pickle.dump(schema, outf)
```