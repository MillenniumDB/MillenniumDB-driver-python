import socket
import warnings
from typing import ByteString

from . import protocol
from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError


class SocketConnection:
    """
    Represents the socket connection to the server.
    """

    def __init__(self, host: str, port: int, scheme: str):
        """
        Create a socket connection with the host and port.
        """
        self._connection_timeout = protocol.DEFAULT_CONNECTION_TIMEOUT
        self._socket = self._create_socket(host, port, scheme)
        self._handshake()

    def sendall(self, data: IOBuffer | ByteString) -> None:
        """
        Send the data to the server.
        """
        if isinstance(data, IOBuffer):
            self._socket.sendall(data.view[: data.num_used_bytes])
        else:
            self._socket.sendall(data)

    def recvall_into(self, iobuffer: IOBuffer, num_bytes: int) -> None:
        """
        Receive the data from the server.
        """
        end = iobuffer.num_used_bytes + num_bytes
        if end > len(iobuffer):
            iobuffer.extend(end - len(iobuffer))

        while iobuffer.num_used_bytes < end:
            num_bytes_recv = self._socket.recv_into(
                iobuffer.view[iobuffer.num_used_bytes : end],
                end - iobuffer.num_used_bytes,
            )

            if num_bytes_recv == 0:
                raise MillenniumDBError("SocketConnection Error: no data received")

            iobuffer.num_used_bytes += num_bytes_recv

    def close(self) -> None:
        """
        Close the socket connection.
        """
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self._socket.close()
        except OSError:
            pass

    def _handshake(self) -> None:
        """
        Perform the handshake with the server
        """
        self._socket.sendall(protocol.DRIVER_PREAMBLE_BYTES)
        response = self._socket.recv(8)
        if response != protocol.SERVER_PREAMBLE_BYTES:
            raise MillenniumDBError("SocketConnection Error: handshake failed")

    def _create_socket(self, host: str, port: int, scheme: str) -> socket.socket:
        try:
            if port is None:
                raise MillenniumDBError("URL does not provide a port")

            allowed_schemes = ("tcp", "ssl", "tls")
            if scheme not in allowed_schemes:
                raise MillenniumDBError(
                    f"Invalid URL scheme: {scheme}. Scheme must be one of the"
                    f" following: {allowed_schemes}"
                )

            if scheme != "tcp":
                warnings.warn(
                    "SSL/TLS is not supported yet. Raw TCP connection will be"
                    " stablished",
                    category=UserWarning,
                )

            sock = socket.create_connection(
                (host, port), timeout=self._connection_timeout
            )
            sock.settimeout(None)
            return sock
        except socket.timeout as e:
            raise MillenniumDBError(
                "SocketConnection Error: socket timed out while establishing connection"
            ) from e
        except Exception as e:
            raise MillenniumDBError(
                f"SocketConnection Error: could not connect to {host}:{port}"
            ) from e
