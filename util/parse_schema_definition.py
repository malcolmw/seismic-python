"""
Author: Malcolm White
Data: Tuesday 20 February 2018

This script parses and pickles Antelope format schema definitions found
in /opt/antelope/$VERSION/data/schema.
Pickling these schemas will make it easy to read and write Antelope style
tables in a general way using Pandas DataFrames.
"""
import argparse
import pickle

def main():
    args = parse_args()
    with open(args.schema) as inf:
        data = inf.read().split(";")
    chunks = [parse_chunk(chunk) for chunk in data]
    schema = {"Attributes": {obj.name: {"dtype": obj.dtype,
                                        "width": obj.width,
                                        "format": obj.fmt,
                                        "null": obj.null}
                             for obj in chunks
                             if isinstance(obj, Attribute)},
              "Relations": {obj.name: obj.fields for obj in chunks
                                                 if isinstance(obj, Relation)}
              }
    print("found", len(schema["Attributes"]), "attributes...")
    print("found", len(schema["Relations"]), "relations...")
    with open(args.output, "wb") as outf:
        print("pickling schema...")
        pickle.dump(schema, outf)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=str, help="schema definition")
    parser.add_argument("output", type=str, help="output pickle")
    return(parser.parse_args())

class Attribute(object):
    def __init__(self, name, dtype, width, fmt, null):
        self.name = name
        self.dtype = dtype
        self.width = width
        self.fmt = fmt
        self.null = null
        print("Attribute:", self.name, self.dtype, self.width, self.fmt, self.null)

class Relation(object):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        print("Relation:", self.name, self.fields)

def parse_chunk(chunk):
    if len(chunk.split()) == 0:
        return(None)
    if chunk.split()[0] == "Attribute":
        return(parse_attribute(chunk))
    elif chunk.split()[0] == "Relation":
        return(parse_relation(chunk))

def parse_attribute(chunk):
    chunk = [line.strip() for line in chunk.strip().split("\n")]
    name, dtype, width, fmt, null = None, None, None, None, None
    for line in chunk:
        if len(line.split()) == 0:
            continue
        if line.split()[0] == "Attribute":
            name = line.split()[1]
        elif line.split()[0] in ("Real", "Integer", "String", "Time", "YearDay") and dtype is None:
            if line.split()[0] == "Real":
                dtype = float
            elif line.split()[0] == "Integer":
                dtype = int
            elif line.split()[0] == "String":
                dtype = str
            elif line.split()[0] == "Time":
                dtype = float
            elif line.split()[0] == "YearDay":
                dtype = int
            width = int("".join(line.split()[1:]).strip("()"))
        elif line.split()[0] == "Format":
            fmt = "".join(line.split()[1:]).strip("()\"")
        elif line.split()[0] == "Null":
            null = "".join(line.split()[1:]).strip("()\"")
    return(Attribute(name, dtype, width, fmt, null))

def parse_relation(chunk):
    chunk = [line.strip() for line in chunk.strip().split("\n")]
    name, fields = None, None
    for line in chunk:
        if len(line.split()) == 0:
            continue
        if line.split()[0] == "Relation":
            name = line.split()[1]
        elif line.split()[0] == "Fields":
            fields = " ".join(line.split()[1:]).strip("()").split()
    return(Relation(name, fields))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc)
        exit(1)
    exit(0)
