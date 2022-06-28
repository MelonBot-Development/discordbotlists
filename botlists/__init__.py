__title__ = "discordbotlists"
__author__ = "japandotorg"
__license__ = "MIT"
__copyright__ = "Copyright 2022 © japandotorg"
__version__ = "1.0.0"

name = "discordbotlists"

from collections import namedtuple

from .base import Base
from .client import Client
from .exceptions import *

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel="alpha", serial=0)
