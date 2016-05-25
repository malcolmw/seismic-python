import os
import sys
__all__ = []
try:
    sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
    import antelope
    __all__ += ["antelope"]
except ImportError:
    _antelope_defined = False
_antelope_defined = True
_datadir = "/home/mcwhite/.local/data/"

__all__ += ["_antelope_defined",
            "_datadir"]
