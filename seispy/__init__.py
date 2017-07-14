import importlib

submodules = ["constants",
              "faults",
              "fm3d",
              "geometry",
              "mapping",
              "sqlschemas",
              "topography",
              "ttgrid",
              "velocity"]
for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy")
