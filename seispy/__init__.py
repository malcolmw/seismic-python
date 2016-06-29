"""
This is top-level documenation. It is coming from seispy/__init__.py doc
string.
"""
import os
import sys

__all__ = []

try:
    sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
    import antelope
    __all__ += ["antelope"]
except ImportError:
    _ANTELOPE_DEFINED = False
_ANTELOPE_DEFINED = True

__all__ += ["_ANTELOPE_DEFINED"]
