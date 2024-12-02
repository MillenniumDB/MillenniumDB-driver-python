from . import protocol
from .iobuffer import IOBuffer


# This class is for build requests
class RequestBuilder:
    """
    This class is for build requests.
    """

    @staticmethod
    def encode_string(string: str) -> bytes:
        """
        :param string: The string to encode.
        :type string: str
        :return: The encoded string in bytes using utf-8.
        """
        return string.encode("utf-8")

    @staticmethod
    def run(query: str) -> IOBuffer:
        """
        Builds a request to execute a query.

        :param query: The query string to execute.
        :type query: str
        :return: The IOBuffer of the request.
        """
        query_bytes = RequestBuilder.encode_string(query)
        query_bytes_length = len(query_bytes)
        iobuffer = IOBuffer(10 + query_bytes_length)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.QUERY)
        iobuffer.write_uint8(protocol.DataType.STRING)
        iobuffer.write_uint32(query_bytes_length)
        iobuffer.write_bytes(query_bytes)
        return iobuffer

    @staticmethod
    def catalog() -> IOBuffer:
        """
        Builds a request to get the catalog.

        :return: The IOBuffer of the request.
        """
        iobuffer = IOBuffer(5)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.CATALOG)
        return iobuffer

    @staticmethod
    def cancel(worker_index: int, cancellation_token: str) -> IOBuffer:
        """
        Builds a request to cancel a query.

        :param worker_index: The index of the worker.
        :type worker_index: int
        :param cancellation_token: The cancellation token.
        :type cancellation_token: str
        :return: The IOBuffer of the request.
        """
        cancellation_token_bytes = RequestBuilder.encode_string(cancellation_token)
        cancellation_token_bytes_length = len(cancellation_token_bytes)
        iobuffer = IOBuffer(15 + cancellation_token_bytes_length)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.CANCEL)
        iobuffer.write_uint8(protocol.DataType.UINT32)
        iobuffer.write_uint32(worker_index)
        iobuffer.write_uint8(protocol.DataType.STRING)
        iobuffer.write_uint32(cancellation_token_bytes_length)
        iobuffer.write_bytes(cancellation_token_bytes)
        return iobuffer
