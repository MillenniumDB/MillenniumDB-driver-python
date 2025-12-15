from functools import wraps
from typing import Any, Dict

from .catalog import Catalog
from .message_receiver import MessageReceiver
from .millenniumdb_error import MillenniumDBError
from .request_buffer import RequestBuffer
from .request_writer import RequestWriter
from .response_handler import ResponseHandler
from .result import Result
from .websocket_connection import WebSocketConnection


def _ensure_session_open(func):
    """
    Ensure that the session is open before executing a function.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._open:
            raise MillenniumDBError("Session Error: session is closed")
        return func(self, *args, **kwargs)

    return wrapper


class Session:
    """
    The class represents a session with the MillenniumDB server.
    """

    def __init__(self, url: str, driver: "Driver"):
        self._driver = driver
        self._open = True
        self._connection = WebSocketConnection(url)
        self._message_receiver = MessageReceiver(self._connection)
        self._request_buffer = RequestBuffer(self._connection)
        self._request_writer = RequestWriter(self._request_buffer)
        self._response_handler = ResponseHandler()

    @_ensure_session_open
    def run(
        self, query: str, parameters: Dict[str, Any] = None, timeout: float = 0.0
    ) -> Result:
        """
        Run a query on the server.
        :return: The result of the query.
        """
        if parameters is None:
            parameters = {}
        return Result(
            self._driver,
            self._connection,
            self._request_writer,
            self._message_receiver,
            self._response_handler,
            query,
            parameters,
            timeout,
        )

    @_ensure_session_open
    def catalog(self) -> Catalog:
        """
        :return: The catalog of the server.
        """
        return Catalog(
            self._connection,
            self._request_writer,
            self._message_receiver,
            self._response_handler,
        )

    @_ensure_session_open
    def _cancel(self, result: Result) -> None:
        """
        Cancel a running query on the server.
        """
        if result.query_preamble is None:
            raise MillenniumDBError("Session Error: query has not been executed yet")

        self._request_writer.write_cancel(
            result.query_preamble["workerIndex"],
            result.query_preamble["cancellationToken"],
        )

    def close(self):
        """
        Close the session.
        """
        if self._open:
            self._open = False
            self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
