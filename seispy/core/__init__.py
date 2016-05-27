"""
This is module level documenation for seispy.core and is coming from
seispy/core/__init__.py
"""
import seispy
from seispy import _antelope_defined

#import exceptions first
from seispy.core.exceptions import ArgumentError,\
                                   InitializationError
#import base classes second
from seispy.core.dbparsable import DbParsable


#import subclasses last
from seispy.core.arrival import Arrival
from seispy.core.channel import Channel
from seispy.core.database import Database
from seispy.core.event import Event
from seispy.core.iterators import EventIterator,\
                                  OriginIterator
from seispy.core.network import Network
from seispy.core.virtualnetwork import VirtualNetwork
from seispy.core.origin import Origin
from seispy.core.station import Station
from seispy.core.trace import Trace
