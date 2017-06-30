import importlib

submodules = ["geometry",
              "topography",
              "ttgrid"]
for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy")
