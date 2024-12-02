from typing import Dict, List, Tuple

from .millenniumdb_error import MillenniumDBError


class Record:
    """
    This class represents an entry in the result of a query.
    """

    def __init__(
        self,
        variables: List[str],
        values: List[object],
        variableToIndex: Dict[str, int],
    ):
        """
        :param length: The number of variables in the record.
        :type length: int
        """
        if len(variables) != len(values):
            raise MillenniumDBError(
                "Record Error: Number of variables does not match the number of values"
            )

        self._variables = variables
        self._values = values
        self._variableToIndex = variableToIndex
        self.length = len(variables)  # The number of variables in the record

    def entries(self) -> List[Tuple[str, object]]:
        """
        Iterate over all entries (key, value).

        :return: an iterable over all entries.
        """
        return [(self._variables[i], self._values[i]) for i in range(len(self))]

    def values(self) -> List[object]:
        """
        Iterate over all values.

        :return: an iterable over all values.
        """
        return self._values

    def __iter__(self):
        """
        Iterate over all values. Equivalent to record.values().

        :yield: an iterable over all values.
        """
        yield from self.values()

    def get(self, key):
        """
        Get the value associated with the key in the record.

        :param key: The variable name or its index.
        :return: The value associated with the key.
        """
        index = key if isinstance(key, int) else self._variableToIndex.get(key, -1)
        if index < 0 or index > len(self._values) - 1:
            raise MillenniumDBError(f"Record Error: Index {index} is out of bounds")
        return self._values[index]

    def has(self, key) -> bool:
        """
        Check if the record has a value associated with the key.

        :param key: The variable name or its index.
        :return: True if the record has a value associated with the key.
        """
        index = key if isinstance(key, int) else self._variableToIndex.get(key, -1)
        return index >= 0 and index < len(self._values)

    def to_dict(self):
        """
        :return: A dictionary representation of the record.
        """
        res = {}
        for i in range(len(self)):
            res[self._variables[i]] = self._values[i]
        return res

    def __str__(self):
        if len(self) == 0:
            return "{}"

        res = "{"
        res += f"{self._variables[0]}: {repr(self._values[0])}"
        for i in range(1, len(self)):
            res += f", {self._variables[i]}: {repr(self._values[i])}"
        return res + "}"

    def __repr__(self):
        """
        :return: A detailed representation of the Record.
        """
        return f"Record<{str(self)}>"

    def __len__(self):
        return self.length
