# coding=utf-8
import importlib

submodules = ["constants",
              "coords",
              "faults",
              "fmm3dio",
              "geogrid",
              "geometry",
              "mapping",
              "stats",
              "surface",
              "topography",
              "ttgrid",
              "velocity",
              "pandas"]
for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy")
