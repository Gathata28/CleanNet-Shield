"""
CleanNet Shield - Adult Content Blocker & Recovery Tool

A comprehensive desktop application that combines multi-layer adult content blocking 
with recovery support tools including streak tracking, journaling, and accountability features.
"""

__version__ = "2.0.0"
__author__ = "CleanNet Shield Team"
__email__ = "support@cleannetshield.com"

# Core modules
from . import core
from . import utils
from . import database

__all__ = [
    "core",
    "utils",
    "database",
    "__version__",
    "__author__",
    "__email__"
]
