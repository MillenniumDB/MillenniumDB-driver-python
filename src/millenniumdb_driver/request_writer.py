import struct
from typing import Any, Dict

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
        # TODO: support more values
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
        # TODO: IMPLEMENT CORRECTLY TO WORK WITH UNSIGNED
        self.write_byte(DataType.INT64)
        self._request_buffer.write(value.to_bytes(8, byteorder="big", signed=True))

    def write_float(self, value: int):
        # TODO: TEST
        self.write_byte(DataType.FLOAT)
        self._request_buffer.write(struct.pack(">f", value))

    def write_string(self, value: str):
        enc = self._encode_string(value, DataType.STRING)
        self._request_buffer.write(enc)

    def _write_parameters(self, parameters: Dict[str, Any]):
        self.write_byte(DataType.MAP)
        self._request_buffer.write(self._encode_size(len(parameters)))
        for key, value in parameters.items():
            if not isinstance(key, str):
                raise MillenniumDBError("Non-string key found at query parameters")
            self.write_string(key)
            try:
                self.write_object(value)
            except MillenniumDBError as e:
                raise MillenniumDBError(
                    "Unsupported value found at query parameters"
                ) from e

    def _encode_string(self, value: str, datatype: DataType) -> bytes:
        value_bytes = value.encode("utf-8")
        res = b""
        res += datatype.to_bytes(1)
        res += self._encode_size(len(value_bytes))
        res += value_bytes
        return res

    def _encode_size(self, value: int) -> bytes:
        return value.to_bytes(4, byteorder="big")
