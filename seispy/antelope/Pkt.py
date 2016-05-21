from seispy import _antelope_defined
if not _antelope_defined:
    raise ImportError("Antelope environment not defined")
from antelope.Pkt import *
