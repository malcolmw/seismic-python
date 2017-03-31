import importlib

submodules = ["geometry",
              "ttgrid"]
for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy")
