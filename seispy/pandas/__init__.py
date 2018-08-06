import importlib

submodules = ['io',
              'catalog',
              'time']

for submodule in submodules:
    importlib.import_module(".{}".format(submodule), package="seispy.pandas")
