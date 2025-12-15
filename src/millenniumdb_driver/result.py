from threading import Thread
from time import sleep
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Tuple

from .message_receiver import MessageReceiver
from .millenniumdb_error import ResultError
from .record import Record
from .request_writer import RequestWriter
from .response_handler import ResponseHandler
from .websocket_connection import WebSocketConnection

if TYPE_CHECKING:
    from pandas import DataFrame

    from .driver import Driver


class Result:
    """
    This class represents the result of a query.
    """

    def __init__(
        self,
        driver: "Driver",
        connection: WebSocketConnection,
        request_writer: RequestWriter,
        message_receiver: MessageReceiver,
        response_handler: ResponseHandler,
        query: str,
        parameters: Dict[str, Any],
        timeout: float,
    ):
        self._driver = driver
        self._connection = connection
        self._variables = []
        self._query_preamble = None
        self._variable_to_index = {}
        self._records = []
        self._summary = None
        self._exception = None
        self._streaming = True
        self._request_writer = request_writer
        self._message_receiver = message_receiver
        self._response_handler = response_handler
        self._run(query, parameters, timeout)

    @property
    def query_preamble(self) -> Any | None:
        """
        :return: query preamble if any, None otherwise
        """
        return self._query_preamble

    def variables(self) -> Tuple[str]:
        """
        :return: The list of variables in the result.
        """
        return self._variables

    def records(self) -> List[Record]:
        """
        :return: The list of records in the result.
        """
        return self._records

    def values(self) -> List[object]:
        """
        :return: The list of values in the result.
        """
        return [record.values() for record in self._records]

    def data(self) -> List[Dict[str, object]]:
        """
        :return: The list of records in the result as dictionaries.
        """
        return [record.to_dict() for record in self._records]

    def to_df(self) -> "DataFrame":
        """
        :return: The result as a pandas DataFrame.
        """
        from pandas import DataFrame  # pylint: disable=import-outside-toplevel

        return DataFrame(self.data())

    def summary(self) -> object | None:
        """
        :return: The summary of the result if any.
        """
        return self._summary

    def error(self) -> Exception | None:
        """
        :return: The exception of the result if any.
        """
        return self._exception

    def __iter__(self) -> Iterator[Record]:
        """
        :return: An iterator over the records in the result.
        """
        return iter(self._records)

    def _try_cancel(self, timeout) -> None:
        sleep(timeout)
        if self._streaming:
            self._driver.cancel(self)

    def _run(self, query: str, parameters: Dict[str, Any], timeout: float) -> None:
        def on_variables(variables, query_preamble) -> None:
            self._variables = variables
            self._query_preamble = query_preamble
            self._variable_to_index = {variables[i]: i for i in range(len(variables))}

            if timeout > 0.0:
                t = Thread(target=self._try_cancel, args=[timeout], daemon=True)
                t.start()

        def on_success(summary) -> None:
            self._summary = summary
            self._streaming = False

        def on_error(error) -> None:
            self._streaming = False
            self._exception = ResultError(self, str(error))
            raise self._exception

        self._response_handler.add_observer(
            {"on_variables": on_variables, "on_error": on_error}
        )
        self._response_handler.add_observer(
            {"on_success": on_success, "on_error": on_error}
        )
        self._request_writer.write_run(query, parameters)
        self._request_writer.flush()

        # on_variables
        message = self._message_receiver.receive()
        self._response_handler.handle(message)

        # on_record / on_success
        raw_records, termination_message = self._message_receiver.receive_records()
        self._records = [
            Record(self._variables, raw_record, self._variable_to_index)
            for raw_record in raw_records
        ]
        self._response_handler.handle(termination_message)
