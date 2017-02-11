from seispy import _ANTELOPE_DEFINED
if not _ANTELOPE_DEFINED:
    raise ImportError("Antelope environment not initialized")
from antelope import brttpkt,\
                     coords,\
                     datascope,\
                     elog,\
                     orb,\
                     Pkt,\
                     stock
import datascope
__all__ = ["brttpkt",
           "coords",
           "datascope",
           "elog",
           "orb",
           "Pkt",
           "stock"]
