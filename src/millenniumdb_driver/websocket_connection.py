from collections.abc import Buffer

import websocket

from . import protocol
from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError


class WebSocketConnection:
    """
    The WebSocket connection is the main class that holds a connection between the client and the server
    """

    def __init__(self, url: str):
        """
        Create a socket connection with the host and port.
        """
        self._ws = self._create_websocket(url)
        self._recv_remainder = bytearray()

    def write(self, data: IOBuffer | Buffer) -> None:
        """
        Send the data to the server.
        """
        if isinstance(data, IOBuffer):
            self._ws.send_binary(data.view[: data.num_used_bytes])
        else:
            self._ws.send_binary(data)

    def close(self) -> None:
        """
        Close the socket connection.
        """
        self._ws.close()

    def recvall_into(self, iobuffer: IOBuffer, num_bytes: int) -> None:
        """
        Receive the data from the server.
        """
        # resize buffer to fit
        end = iobuffer.num_used_bytes + num_bytes
        if end > len(iobuffer):
            iobuffer.extend(end - len(iobuffer))

        # consume remainder if any
        if len(self._recv_remainder) > 0:
            rem = self._recv_remainder
            needed = end - iobuffer.num_used_bytes

            if len(rem) > needed:
                # portion of remainder fits
                iobuffer.write_bytes(rem[:needed])
                self._recv_remainder = rem[needed:]
                return

            # all remainder fits
            iobuffer.write_bytes(rem)
            self._recv_remainder = bytearray()

        while iobuffer.num_used_bytes < end:
            data = self._ws.recv()
            if not data:
                raise MillenniumDBError("SocketConnection Error: no data received")

            needed = end - iobuffer.num_used_bytes

            if len(data) > needed:
                # portion fits ,store remainder
                iobuffer.write_bytes(data[:needed])
                self._recv_remainder = data[needed:]
                return

            # all data fits
            iobuffer.write_bytes(data)

    def _create_websocket(self, url: str) -> websocket.WebSocket:
        try:
            ws = websocket.create_connection(
                url,
                timeout=protocol.DEFAULT_CONNECTION_TIMEOUT,
            )
            return ws
        except websocket.WebSocketException as e:
            raise MillenniumDBError(f"WebSocket Connection Error: {e}") from e
        except Exception as e:
            raise MillenniumDBError(
                f"WebSocket Connection Error: could not connect to {url}"
            ) from e
