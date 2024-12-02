from enum import IntEnum, auto

DRIVER_PREAMBLE_BYTES = b"MDB_DRVR"
SERVER_PREAMBLE_BYTES = b"MDB_SRVR"

DEFAULT_CONNECTION_TIMEOUT = 20.0


class ModelId(IntEnum):
    QUAD_MODEL_ID = 0
    RDF_MODEL_ID = auto()

    TOTAL = auto()


class DataType(IntEnum):
    NULL = 0
    BOOL_FALSE = auto()
    BOOL_TRUE = auto()
    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    UINT64 = auto()
    INT64 = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DECIMAL = auto()
    STRING = auto()
    STRING_LANG = auto()
    STRING_DATATYPE = auto()
    IRI = auto()
    NAMED_NODE = auto()
    EDGE = auto()
    ANON = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()
    PATH = auto()
    LIST = auto()
    MAP = auto()

    TOTAL = auto()


class RequestType(IntEnum):
    QUERY = 0
    CATALOG = auto()
    CANCEL = auto()
    UPDATE = auto()
    AUTH = auto()

    TOTAL = auto()


class ResponseType(IntEnum):
    SUCCESS = 0
    ERROR = auto()
    RECORD = auto()
    VARIABLES = auto()

    TOTAL = auto()
