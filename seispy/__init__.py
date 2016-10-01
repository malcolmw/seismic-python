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
    sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
    import antelope.datascope as datascope
    __all__ += ["datascope"]
    _ANTELOPE_DEFINED = True
except (ImportError, KeyError):
    _ANTELOPE_DEFINED = False

__all__ += ["_ANTELOPE_DEFINED"]
