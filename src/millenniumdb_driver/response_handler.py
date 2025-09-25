from typing import Callable, Dict, List

from . import protocol
from .millenniumdb_error import MillenniumDBError


class ResponseHandler:
    """
    This class handles the responses coming from the server.
    """

    def __init__(self):
        self._current_observer: Dict[str, Callable] = None
        self._pending_observers: List[Dict[str, Callable]] = []

    def handle(self, message: Dict[str, object]) -> None:
        """
        Handle an incoming response.

        :param message: The incoming message.
        :type message: Dict[str, object]
        """
        match message["type"]:
            case protocol.ResponseType.SUCCESS:
                self._callback("on_success", message["payload"])

            case protocol.ResponseType.ERROR:
                self._callback("on_error", MillenniumDBError(message["payload"]))

            case protocol.ResponseType.VARIABLES:
                variables = message["payload"]["variables"]
                query_preamble = message["payload"]["queryPreamble"]
                self._callback("on_variables", variables, query_preamble)

            case _:
                raise NotImplementedError

    def add_observer(self, observer: Dict[str, Callable]) -> None:
        """
        Enqueue a new observer for handling a response.

        :param observer: that will handle the received data.
        :type observer: Dict[str, Callable
        """
        if self._current_observer is None:
            self._current_observer = observer
        else:
            self._pending_observers.append(observer)

    def _callback(self, callback_key: str, *args, **kwargs) -> None:
        """
        Call the observer with the given key and arguments and advance to the next one.

        :param callback_key: The key of the observer to call.
        :type callback_key: str
        """
        if (
            self._current_observer is not None
            and callback_key in self._current_observer
        ):
            tmp_observer = self._current_observer

            # advance current observer
            if len(self._pending_observers) > 0:
                self._current_observer = self._pending_observers.pop(0)
            else:
                self._current_observer = None

            # handle callback
            tmp_observer[callback_key](*args, **kwargs)
