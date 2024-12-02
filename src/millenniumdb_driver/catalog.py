from . import protocol
from .message_receiver import MessageReceiver
from .millenniumdb_error import MillenniumDBError
from .request_builder import RequestBuilder
from .response_handler import ResponseHandler
from .socket_connection import SocketConnection


class Catalog:
    """
    This class represents the catalog of the MillenniumDB server.
    """

    def __init__(
        self,
        connection: SocketConnection,
        message_receiver: MessageReceiver,
        response_handler: ResponseHandler,
    ):
        """
        :param connection: The socket connection.
        :type connection: SocketConnection
        :param message_receiver: The receiver of incoming messages.
        :type message_receiver: MessageReceiver
        :param response_handler: The handler of the responses.
        :type response_handler: ResponseHandler
        """
        self._connection = connection
        self._message_receiver = message_receiver
        self._response_handler = response_handler
        self._model_id = None
        self._version = None
        self._catalog()

    @property
    def model_id(self) -> int:
        """
        :return: The model ID of the server.
        """
        return self._model_id

    @property
    def version(self) -> int:
        """
        :return: The version of the server.
        """
        return self._version

    def _catalog(self):
        """
        Set the model ID and version of the server
        Add success and error observers to the response handler
        """

        def on_success(summary) -> None:
            self._model_id = summary["modelId"]
            self._version = summary["version"]

        def on_error(error) -> None:
            raise error

        self._response_handler.add_observer(
            {"on_success": on_success, "on_error": on_error}
        )
        self._connection.sendall(RequestBuilder.catalog())

        message = self._message_receiver.receive()
        self._response_handler.handle(message)

    def _model_id_to_str(self, model_id: int) -> str:
        match model_id:
            case protocol.ModelId.QUAD_MODEL_ID:
                return "quad"

            case protocol.ModelId.RDF_MODEL_ID:
                return "rdf"

            case _:
                return "unknown"

    def __repr__(self) -> str:
        """
        :return: A string representation of the Catalog object.
        """
        return f"Catalog<{self._model_id_to_str(self._model_id)}, v{self._version}>"
