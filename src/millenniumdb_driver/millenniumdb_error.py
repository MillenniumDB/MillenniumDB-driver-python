class MillenniumDBError(Exception):
    """
    This class represents an error that has been thrown by the driver
    """

    pass


class ResultError(MillenniumDBError):
    """
    This specific error is thrown when an error occurs while processing a result
    in order to be able to consume the results obtained so far

    :ivar result: The result object that was being processed
    :vartype result: Result
    """

    def __init__(self, result: "Result", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: "Result" = result
