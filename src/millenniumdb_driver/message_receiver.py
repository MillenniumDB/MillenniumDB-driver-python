from typing import Any, List, Tuple

from . import protocol
from .chunk_decoder import ChunkDecoder
from .iobuffer import IOBuffer
from .message_decoder import MessageDecoder
from .socket_connection import SocketConnection


class MessageReceiver:
    """
    Represents the receiver of the incoming messages.
    """

    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection):
        """
        :param connection: The socket connection.
        :type connection: SocketConnection
        """
        self._receiver_buffer = IOBuffer()
        self._chunk_decoder = ChunkDecoder(connection, self._receiver_buffer)
        self._message_decoder = MessageDecoder(self._receiver_buffer)

    def receive(self) -> object:
        """
        Decode and return the incoming message

        :return: The decoded message.
        """
        # Decode chunks
        self._chunk_decoder.decode()

        # Decode message
        msg = self._message_decoder.decode()

        # Reset receiver buffer for the next message
        self._receiver_buffer.reset()

        return msg

    def receive_records(self) -> Tuple[List[object], Any]:
        """
        Receive and decode the incoming records.

        :return: The decoded records and the last message.
        """
        records = []

        msg = self.receive()
        while msg["type"] == protocol.ResponseType.RECORD:
            records.append(msg["payload"])
            msg = self.receive()

        return records, msg
