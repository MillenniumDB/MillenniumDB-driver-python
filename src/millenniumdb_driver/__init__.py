from .driver import Driver as _Driver
from .millenniumdb_error import MillenniumDBError, ResultError


__version__ = "0.0.1"


def driver(url: str) -> _Driver:
    return _Driver(url)


__all__ = ["driver", "MillenniumDBError", "ResultError"]
