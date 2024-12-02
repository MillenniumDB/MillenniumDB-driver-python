import struct


class IOBuffer:
    """
    The class IOBuffer can be used to read and write data to and from a binary buffer.\n

    Data itself should not be manipulated appart from extend method.\n

    Data view is what will be sliced, written and read\n

    :ivar view: The memoryview of the buffer.
    :vartype view: memoryview
    :ivar num_used_bytes: The number of used bytes in the buffer.
    :vartype num_used_bytes: int
    """

    DEFAULT_INITIAL_BUFFER_SIZE = 4096

    def __init__(self, initial_buffer_size: int = DEFAULT_INITIAL_BUFFER_SIZE):
        """
        :param initial_buffer_size: The initial size of the buffer.
        :type initial_buffer_size: int
        """
        self._buffer = bytearray(initial_buffer_size)
        self._current_read_position = 0
        self.view = memoryview(self._buffer)
        self.num_used_bytes = 0

    def extend(self, num_bytes: int) -> None:
        """
        Extend the buffer by num_bytes.
        """
        self._buffer += bytearray(num_bytes)
        self.view = memoryview(self._buffer)

    def reset(self) -> None:
        """
        Reset the buffer.
        """
        self.num_used_bytes = 0
        self._current_read_position = 0

    def __len__(self):
        return len(self._buffer)

    def read_uint8(self) -> int:
        """
        :return: The uint8 read from the buffer.
        """
        return self.view[self._update_current_read_position(1)]

    def read_uint32(self) -> int:
        """
        :return: The uint32 read from the buffer.
        """
        return int.from_bytes(self.read_bytes(4), "big", signed=False)

    def read_uint64(self) -> int:
        """
        :return: The uint64 read from the buffer.
        """
        return int.from_bytes(self.read_bytes(8), "big", signed=False)

    def read_int64(self) -> int:
        """
        :return: The int64 read from the buffer.
        """
        return int.from_bytes(self.read_bytes(8), "big", signed=True)

    def read_float(self) -> float:
        """
        :return: The float read from the buffer.
        """
        return struct.unpack(">f", self.read_bytes(4))[0]

    def read_double(self) -> float:
        """
        :return: The double read from the buffer.
        """
        return struct.unpack(">d", self.read_bytes(8))[0]

    def read_string(self, num_bytes: int) -> str:
        """
        :param num_bytes: The number of bytes to read.
        :type num_bytes: int
        :return: The string read from the buffer.
        """
        return str(self.read_bytes(num_bytes), "utf-8")

    def read_bytes(self, num_bytes: int) -> memoryview:
        """
        :param num_bytes: The number of bytes to read.
        :type num_bytes: int
        :return: The bytes read from the buffer.
        """
        return self.view[
            self._update_current_read_position(num_bytes) : self._current_read_position
        ]

    def write_uint8(self, value: int) -> None:
        """
        Write an uint8 to the buffer.

        :param value: The uint8 to write.
        :type value: int
        """
        self.view[self._update_num_used_bytes(1)] = value

    def write_uint32(self, value: int) -> None:
        """
        Write an uint32 to the buffer.

        :param value: The uint32 to write.
        :type value: int
        """
        self.view[self._update_num_used_bytes(4) : self.num_used_bytes] = (
            value.to_bytes(4, "big", signed=False)
        )

    def write_bytes(self, value: bytes) -> None:
        """
        Write bytes to the buffer.

        :param value: The bytes to write.
        :type value: bytes
        """
        self.view[self._update_num_used_bytes(len(value)) : self.num_used_bytes] = value

    def pop_uint16(self) -> int:
        """
        :return: The uint16 popped from the end of the used buffer, removing its used bytes.
        """
        res = (
            self.view[self.num_used_bytes - 2] << 8 | self.view[self.num_used_bytes - 1]
        )
        self.num_used_bytes -= 2
        return res

    def _update_current_read_position(self, num_bytes: int) -> int:
        previous_read_position = self._current_read_position
        self._current_read_position += num_bytes
        return previous_read_position

    def _update_num_used_bytes(self, num_bytes: int) -> None:
        previous_used_bytes = self.num_used_bytes
        self.num_used_bytes += num_bytes
        return previous_used_bytes
