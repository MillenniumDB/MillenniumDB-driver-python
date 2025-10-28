import importlib.metadata

from . import graph_objects
from .driver import Driver as _Driver
from .millenniumdb_error import MillenniumDBError, ResultError

__version__ = importlib.metadata.version("millenniumdb_driver")


def driver(url: str) -> _Driver:
    return _Driver(url)


__all__ = ["driver", "MillenniumDBError", "ResultError"]
