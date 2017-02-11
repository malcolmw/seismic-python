"""
This is top-level documenation. It is coming from seispy/__init__.py doc
string.
"""
import importlib
import os
import sys

import seispy.log
log.initialize_logging(__name__)

__all__ = []


submodules = ["burrow",
              "event",
              "gather",
              "geoid",
              "geometry",
              "locate",
              "network",
              "station",
              "trace",
              "ttgrid",
              "util",
              "velocity"]

try:
    sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
    import antelope.datascope as datascope
    __all__ += ["datascope"]
    _ANTELOPE_DEFINED = True
except (ImportError, KeyError):
    _ANTELOPE_DEFINED = False

for module in submodules:
    importlib.import_module(".%s" % module, package="seispy")

__all__ += submodules

__all__ += ["_ANTELOPE_DEFINED"]

