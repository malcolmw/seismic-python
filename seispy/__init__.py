"""
This is top-level documenation. It is coming from seispy/__init__.py doc
string.
"""
import os
import site
import sys

site.addsitedir("/usr/lib64/python2.7/site-packages")

__all__ = []

try:
    sys.path.append('%s/data/python/antelope' % os.environ['ANTELOPE'])
    import antelope
    __all__ += ["antelope"]
except (ImportError, KeyError):
    _ANTELOPE_DEFINED = False
_ANTELOPE_DEFINED = True

__all__ += ["_ANTELOPE_DEFINED"]
