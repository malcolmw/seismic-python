import importlib

submodules = ["fixed_width",
              "schema",
              "special"]

for submodule in submodules:
    importlib.import_module(".{}".format(submodule),
                            package="seispy.pandas.io")
