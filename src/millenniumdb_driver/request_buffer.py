from typing import ByteString

from .protocol import BUFFER_SIZE, CHUNK_HEADER_SIZE
from .websocket_connection import WebSocketConnection

# Packet format:
#     [chunk_size][      chunk     ]
#     [ 2 bytes  ][chunk_size bytes]
#
# The seal that marks the end of a message is a "zero-sized chunk" [0x00 0x00]


class RequestBuffer:

    def __init__(self, connection: WebSocketConnection):
        self._connection = connection
        self._current_pos = 0
        self._chunk_open = False
        self._current_chunk_start_pos = 0
        self._buffer = bytearray(BUFFER_SIZE)
        self._view = memoryview(self._buffer)

    def write(self, data: ByteString) -> None:
        remaining_write = len(data)
        offset = 0

        while remaining_write > 0:
            self._ensure_write_space()

            max_space = self._remaining_space()
            if remaining_write > max_space:
                # flush the data that fits in the buffer and continue with the rest
                self._view[self._current_pos : self._current_pos + max_space] = data[
                    offset : offset + max_space
                ]
                self._current_pos += max_space
                offset += max_space
                remaining_write -= max_space
                self.flush()
            else:
                # all remaining data fits in the buffer
                self._view[self._current_pos : self._current_pos + remaining_write] = (
                    data[offset : offset + remaining_write]
                )
                self._current_pos += remaining_write
                break

    def seal(self) -> None:
        if self._chunk_open:
            self._close_chunk()

        if self._remaining_space() < CHUNK_HEADER_SIZE:
            self.flush()

        self._view[self._current_pos] = 0
        self._view[self._current_pos + 1] = 0
        self._current_pos += 2

    def flush(self) -> None:
        if self._chunk_open:
            self._close_chunk()

        if self._current_pos > 0:
            self._connection.write(self._view[: self._current_pos])
            self._current_pos = 0

    def _open_chunk(self) -> None:
        self._current_chunk_start_pos = self._current_pos
        self._current_pos += CHUNK_HEADER_SIZE
        self._chunk_open = True

    def _close_chunk(self) -> None:
        chunk_size = (
            self._current_pos - self._current_chunk_start_pos - CHUNK_HEADER_SIZE
        )
        self._view[self._current_chunk_start_pos] = (chunk_size >> 8) & 0xFF
        self._view[self._current_chunk_start_pos + 1] = chunk_size & 0xFF
        self._chunk_open = False

    def _ensure_write_space(self) -> None:
        num_bytes = 1 if self._chunk_open else CHUNK_HEADER_SIZE + 1
        if self._remaining_space() < num_bytes:
            self.flush()

        if not self._chunk_open:
            self._open_chunk()

    def _remaining_space(self) -> int:
        return BUFFER_SIZE - self._current_pos
