from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError
from .socket_connection import SocketConnection


class ChunkDecoder:
    """
    Decode the incoming chunks from the server.
    """

    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection, iobuffer: IOBuffer):
        """
        :param connection: The socket connection.
        :type connection: SocketConnection
        :param iobuffer: The IOBuffer.
        :type iobuffer: IOBuffer
        """
        self._connection = connection
        self._iobuffer = iobuffer

    def decode(self):
        """
        Initialize the decoding loop until the SEAL is received.
        """
        try:
            # Get first chunk size
            self._connection.recvall_into(self._iobuffer, 2)
            chunk_size = self._iobuffer.pop_uint16()

            # Decode all the chunks until we reach the SEAL
            while chunk_size != ChunkDecoder.SEAL:
                # Receive current chunk and next chunk size in the same recv call
                self._connection.recvall_into(
                    self._iobuffer,
                    chunk_size + 2,
                )
                chunk_size = self._iobuffer.pop_uint16()

        except Exception as e:
            raise MillenniumDBError("ChunkDecoder Error: could not decode chunk") from e
