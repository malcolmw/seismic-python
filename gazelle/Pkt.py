from seispy import _ANTELOPE_DEFINED
if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not defined")
from antelope.Pkt import *
