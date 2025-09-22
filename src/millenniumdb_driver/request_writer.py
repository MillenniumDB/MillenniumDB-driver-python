from typing import Any, Dict

from .millenniumdb_error import MillenniumDBError
from .protocol import DataType, RequestType
from .request_buffer import RequestBuffer


class RequestWriter:
    def __init__(self, request_buffer: RequestBuffer):
        self._request_buffer = request_buffer

    def write_run(self, query: str, parameters: Dict[str, Any]) -> None:
        self.write_uint8(RequestType.QUERY)
        self.write_string(query)
        self._write_parameters(parameters)
        self._request_buffer.seal()

    def write_catalog(self) -> None:
        self.write_uint8(RequestType.CATALOG)
        self._request_buffer.seal()

    def write_cancel(self, worker_index: int, cancellation_token: str) -> None:
        self.write_uint8(RequestType.CANCEL)
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
        else:
            raise MillenniumDBError(
                f"RequestWriter Error: Unsupported type: {type(value)}"
            )

    def write_null(self):
        self.write_uint8(DataType.NULL)

    def write_bool(self, value: bool):
        self.write_uint8(DataType.BOOL_TRUE if value else DataType.BOOL_FALSE)

    def write_uint8(self, value: int):
        self._request_buffer.write(value.to_bytes(1))

    def write_uint32(self, value: int):
        self._request_buffer.write(value.to_bytes(4, byteorder="big"))

    def write_string(self, value: str):
        enc = self._encode_string(value, DataType.STRING)
        self._request_buffer.write(enc)

    def _write_parameters(self, parameters: Dict[str, Any]):
        self.write_uint8(DataType.MAP)
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
