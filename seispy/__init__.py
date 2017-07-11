import importlib

submodules = ["constants",
              "fm3d",
              "geometry",
              "sqlschemas",
              "topography",
              "ttgrid",
              "velocity"]
for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy")
