from threading import Thread
from time import sleep
from typing import Dict, Iterator, List, Tuple

from .message_receiver import MessageReceiver
from .millenniumdb_error import ResultError
from .record import Record
from .request_builder import RequestBuilder
from .response_handler import ResponseHandler
from .socket_connection import SocketConnection


class Result:
    """
    This class represents the result of a query.
    """

    def __init__(
        self,
        driver: "Driver",
        connection: SocketConnection,
        message_receiver: MessageReceiver,
        response_handler: ResponseHandler,
        query: str,
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
        self._message_receiver = message_receiver
        self._response_handler = response_handler
        self._run(query, timeout)

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
        from pandas import DataFrame

        return DataFrame(self.data())

    def summary(self) -> object:
        """
        :return: The summary of the result.
        """
        return self._summary

    def __iter__(self) -> Iterator[Record]:
        """
        :return: An iterator over the records in the result.
        """
        return iter(self._records)

    def _try_cancel(self, timeout) -> None:
        sleep(timeout)
        if self._streaming:
            self._driver.cancel(self)

    def _run(self, query: str, timeout: float) -> None:
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
            self._exception = error
            raise ResultError(self) from self._exception

        self._response_handler.add_observer(
            {"on_variables": on_variables, "on_error": on_error}
        )
        self._response_handler.add_observer(
            {"on_success": on_success, "on_error": on_error}
        )
        self._connection.sendall(RequestBuilder.run(query))

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
