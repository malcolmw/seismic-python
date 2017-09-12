import importlib

submodules = ["fmm3d"]

for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="wavefront")
