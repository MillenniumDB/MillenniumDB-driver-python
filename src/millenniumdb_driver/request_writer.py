import struct
from typing import Any, Dict

import numpy as np
from numpy.typing import NDArray

from .graph_objects import (
    IRI,
    GraphAnon,
    GraphEdge,
    GraphNode,
    StringDatatype,
    StringLang,
)
from .millenniumdb_error import MillenniumDBError
from .protocol import DataType, RequestType
from .request_buffer import RequestBuffer


class RequestWriter:
    """
    This class handles the request writing from the client to the server
    """

    def __init__(self, request_buffer: RequestBuffer):
        self._request_buffer = request_buffer

    def write_run(self, query: str, parameters: Dict[str, Any]) -> None:
        self.write_byte(RequestType.QUERY)
        self.write_string(query)
        self._write_parameters(parameters)
        self._request_buffer.seal()

    def write_catalog(self) -> None:
        self.write_byte(RequestType.CATALOG)
        self._request_buffer.seal()

    def write_cancel(self, worker_index: int, cancellation_token: str) -> None:
        self.write_byte(RequestType.CANCEL)
        self.write_uint32(worker_index)
        self.write_string(cancellation_token)
        self._request_buffer.seal()

    def flush(self) -> None:
        self._request_buffer.flush()

    def write_object(self, value: Any):
        # Common
        if value is None:
            self.write_null()
        elif isinstance(value, bool):
            self.write_bool(value)
        elif isinstance(value, str):
            self.write_string(value)
        elif isinstance(value, int):
            self.write_int64(value)
        elif isinstance(value, float):
            self.write_float(value)
        elif isinstance(value, GraphAnon):
            self.write_anon(value.id)
        elif isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise MillenniumDBError(
                    "RequestWriter Error: Tensors must have exactly one dimension"
                )

            if value.dtype == np.float32:
                self.write_tensor(value, DataType.FLOAT)
            elif value.dtype == np.float64:
                self.write_tensor(value, DataType.DOUBLE)
            else:
                raise MillenniumDBError(
                    f"RequestWriter Error: Unsupported tensor dtype: {value.dtype}"
                )
        # MQL
        elif isinstance(value, GraphNode):
            self.write_named_node(value.id)
        elif isinstance(value, GraphEdge):
            self.write_edge(value.id)
        # SPARQL
        elif isinstance(value, IRI):
            self.write_iri(value)
        elif isinstance(value, StringLang):
            self.write_string_lang(value)
        elif isinstance(value, StringDatatype):
            self.write_string_datatype(value)
        else:
            raise MillenniumDBError(
                f"RequestWriter Error: Unsupported type: {type(value)}"
            )

    def write_null(self):
        self.write_byte(DataType.NULL)

    def write_bool(self, value: bool):
        self.write_byte(DataType.BOOL_TRUE if value else DataType.BOOL_FALSE)

    def write_byte(self, value: int):
        self._request_buffer.write(value.to_bytes(1))

    def write_uint32(self, value: int):
        self._request_buffer.write(value.to_bytes(4, byteorder="big"))

    def write_int64(self, value: int):
        self.write_byte(DataType.INT64)
        self._request_buffer.write(value.to_bytes(8, byteorder="big", signed=value < 0))

    def write_float(self, value: int):
        self.write_byte(DataType.FLOAT)
        self._request_buffer.write(struct.pack(">f", value))

    def write_named_node(self, value: str):
        enc = self._encode_typed_string(value, DataType.NAMED_NODE)
        self._request_buffer.write(enc)

    def write_edge(self, value: int):
        self.write_byte(DataType.EDGE)
        self._request_buffer.write(value.to_bytes(8, byteorder="big"))

    def write_anon(self, value: int):
        self.write_byte(DataType.ANON)
        self._request_buffer.write(value.to_bytes(8, byteorder="big"))

    def write_string(self, value: str):
        enc = self._encode_typed_string(value, DataType.STRING)
        self._request_buffer.write(enc)

    def write_iri(self, value: IRI):
        enc = self._encode_typed_string(value.iri, DataType.IRI)
        self._request_buffer.write(enc)

    def write_string_lang(self, value: StringLang):
        enc = self._encode_typed_string(value.str, DataType.STRING_LANG)
        enc += self._encode_bytes(value.lang.encode("utf-8"))
        self._request_buffer.write(enc)

    def write_string_datatype(self, value: StringDatatype):
        enc = self._encode_typed_string(value.str, DataType.STRING_DATATYPE)
        enc += self._encode_bytes(value.datatype.iri.encode("utf-8"))
        self._request_buffer.write(enc)

    def write_tensor(
        self,
        value: NDArray[np.float32] | NDArray[np.float64],
        tensor_datatype: DataType,
    ):
        # write contiguos array of floating points in big endian
        self.write_byte(DataType.TENSOR)
        self.write_byte(tensor_datatype)
        enc = self._encode_size(value.size)
        enc += value.astype(value.dtype.newbyteorder(">")).tobytes()
        self._request_buffer.write(enc)

    def _write_parameters(self, parameters: Dict[str, Any]):
        self.write_byte(DataType.MAP)
        self._request_buffer.write(self._encode_size(len(parameters)))
        for key, value in parameters.items():
            if not isinstance(key, str):
                raise MillenniumDBError("Non-string key found at query parameters")
            self.write_string(key)
            self.write_object(value)

    def _encode_typed_string(self, value: str, datatype: DataType) -> bytes:
        value_bytes = value.encode("utf-8")
        res = b""
        res += datatype.to_bytes(1)
        res += self._encode_bytes(value_bytes)
        return res

    def _encode_bytes(self, value: bytes) -> bytes:
        res = b""
        res = self._encode_size(len(value))
        res += value
        return res

    def _encode_size(self, value: int) -> bytes:
        return value.to_bytes(4, byteorder="big")
