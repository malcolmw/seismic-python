import argparse
import os
import seispy

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dbin", type=str, help="input database")
    parser.add_argument("dbout", type=str, help="output database")
    return(parser.parse_args())

def main():
    args = parse_args()
    cat = seispy.pandas.catalog.Catalog(os.path.abspath(args.dbin),
                                        fmt="fwf",
                                        schema="css3.0")
    cat.save(os.path.abspath(args.dbout))

if __name__ == "__main__":
    main()
