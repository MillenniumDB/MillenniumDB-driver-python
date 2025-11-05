from enum import IntEnum, auto

DRIVER_PREAMBLE_BYTES = b"MDB_DRVR"
SERVER_PREAMBLE_BYTES = b"MDB_SRVR"

DEFAULT_CONNECTION_TIMEOUT = 20.0


#  Packet format:
#  [chunk_size][      chunk     ]
#  [ 2 bytes  ][chunk_size bytes]
#
#  The seal that marks the end of a message is a "zero-sized chunk" [0x00 0x00]
#
#  Theoretically the maximum chunk size is 65'535 bytes, but our buffer size is 1400 for optimizing the MTU
#  src: https://superuser.com/questions/343107/mtu-is-1500-why-the-first-fragment-length-is-1496-in-ipv6
#
#  We could write more than one chunk in the same buffer. It is expected that the Session and its handlers
#  manage the flushing manually if this is not intended.
BUFFER_SIZE = 1400
CHUNK_HEADER_SIZE = 2


class ModelId(IntEnum):
    QUAD_MODEL_ID = 0
    RDF_MODEL_ID = auto()
    GQL_MODEL_ID = auto()

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
    TENSOR = auto()

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
