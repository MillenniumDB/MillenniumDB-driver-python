from typing import List, Literal


class GraphNode:
    """
    Represents a node in the graph.

    :ivar id: The node identifier.
    :vartype id: str
    """

    def __init__(self, id_: str):
        """
        attributes:
        id (str): The node identifier
        """
        self.id = id_

    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the GraphNode.
        """
        return f"GraphNode<{str(self)}>"


class GraphEdge:
    """
    Represents an edge in the graph.

    :ivar id: The edge identifier.
    :vartype id: int
    """

    def __init__(self, id_: int):
        """
        attributes:
        id (int): The edge identifier
        """
        self.id = id_

    def __str__(self):
        return f"_e{self.id}"

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the GraphEdge.
        """
        return f"GraphEdge<{str(self)}>"


class GraphAnon:
    """
    Represents an anonymous node in the graph.

    :ivar id: The anonymous node identifier.
    :vartype id: int
    """

    def __init__(self, id_: int):
        """
        attributes:
        id (int): The anonymous node identifier
        """
        self.id = id_

    def __str__(self):
        return f"_a{self.id}"

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the GraphAnon.
        """
        return f"GraphAnon<{str(self)}>"


class SimpleDate:
    """
    Represents a simple date.

    :ivar year: The year of the date.
    :vartype year: int
    :ivar month: The month of the date.
    :vartype month: int
    :ivar day: The day of the date.
    :vartype day: int
    :ivar tz_minute_offset: The timezone offset in minutes.
    :vartype tz_minute_offset: int
    """

    def __init__(self, year: int, month: int, day: int, tz_minute_offset: int):
        self.year = year
        self.month = month
        self.day = day
        self.tz_minute_offset = tz_minute_offset

    def __str__(self):
        year = str(self.year)
        month = str(self.month).zfill(2)
        day = str(self.day).zfill(2)
        res = f"{year}-{month}-{day}"
        if self.tz_minute_offset == 0:
            res += "Z"
        else:
            tz_hour = self.tz_minute_offset // 60
            tz_min = self.tz_minute_offset % 60
            res += "-" if self.tz_minute_offset < 0 else "+"
            res += str(abs(tz_hour)).zfill(2) + ":"
            res += str(abs(tz_min)).zfill(2)
        return res

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the SimpleDate.
        """
        return f"SimpleDate<{str(self)}>"


class Time:
    """
    Represents a time.

    :ivar hour: The hour of the time.
    :vartype hour: int
    :ivar minute: The minute of the time.
    :vartype minute: int
    :ivar second: The second of the time.
    :vartype second: int
    :ivar tz_minute_offset: The timezone offset in minutes.
    :vartype tz_minute_offset: int
    """

    def __init__(self, hour: int, minute: int, second: int, tz_minute_offset: int):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tz_minute_offset = tz_minute_offset

    def __str__(self):
        hour = str(self.hour).zfill(2)
        minute = str(self.minute).zfill(2)
        second = str(self.second).zfill(2)
        res = f"{hour}:{minute}:{second}"
        if self.tz_minute_offset == 0:
            res += "Z"
        else:
            tz_hour = self.tz_minute_offset // 60
            tz_min = self.tz_minute_offset % 60
            res += "-" if self.tz_minute_offset < 0 else "+"
            res += str(abs(tz_hour)).zfill(2) + ":"
            res += str(abs(tz_min)).zfill(2)
        return res

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the Time.
        """
        return f"Time<{str(self)}>"


class DateTime:
    """
    Represents a datetime.

    :ivar year: The year of the datetime.
    :vartype year: int
    :ivar month: The month of the datetime.
    :vartype month: int
    :ivar day: The day of the datetime.
    :vartype day: int
    :ivar hour: The hour of the datetime.
    :vartype hour: int
    :ivar minute: The minute of the datetime.
    :vartype minute: int
    :ivar second: The second of the datetime.
    :vartype second: int
    :ivar tz_minute_offset: The timezone offset in minutes.
    :vartype tz_minute_offset: int
    """

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        tz_minute_offset: int,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tz_minute_offset = tz_minute_offset

    def __str__(self) -> str:
        year = str(self.year)
        month = str(self.month).zfill(2)
        day = str(self.day).zfill(2)
        hour = str(self.hour).zfill(2)
        minute = str(self.minute).zfill(2)
        second = str(self.second).zfill(2)
        res = f"{year}-{month}-{day}T{hour}:{minute}:{second}"
        if self.tz_minute_offset == 0:
            res += "Z"
        else:
            tzHour = self.tz_minute_offset // 60
            tzMin = self.tz_minute_offset % 60
            res += "-" if self.tz_minute_offset < 0 else "+"
            res += str(abs(tzHour)).zfill(2) + ":"
            res += str(abs(tzMin)).zfill(2)
        return res

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the DateTime.
        """
        return f"DateTime<{str(self)}>"


Direction = Literal["left", "right", "undirected"]


class GraphPathSegment:
    """
    Represents a segment in the path.\n

    :ivar source: The starting node of the segment.
    :vartype source: object
    :ivar target: The ending node of the segment.
    :vartype target: object
    :ivar edge_type: The type of the segment.
    :vartype edge_type: object
    :ivar direction: The direction of the segment
    :vartype direction: str
    """

    def __init__(
        self, source: object, target: object, edge_type: object, direction: Direction
    ) -> None:
        """
        attributes:
        source (object): The starting node of the segment
        target (object): The ending node of the segment
        edge_type (object): The type of the segment
        direction (Direction): The direction of the segment
        """
        self.source = source
        self.target = target
        self.edge_type = edge_type
        self.direction = direction

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the GraphPath.
        """
        return (
            f"GraphPathSegment<source={self.source}, target={self.target},"
            f" edge_type={self.edge_type}, direction={self.direction}>"
        )


class GraphPath:
    """
    Represents a path in the graph.

    :ivar start: The starting node of the path.
    :vartype start: object
    :ivar end: The ending node of the path.
    :vartype end: object
    :ivar segments: The segments of the path.
    :vartype segments: List[GraphPathSegment]
    :ivar length: The number of segments in the path.
    :vartype length: int
    """

    def __init__(
        self,
        start: object,
        end: object,
        segments: List[GraphPathSegment],
    ) -> None:
        """
        attributes:
        start (object): The starting node of the path
        end (object): The ending node of the path
        segments (List[GraphPathSegment]): The segments of the path
        length (int): The number of segments in the path
        """
        self.start = start
        self.end = end
        self.segments = segments
        self.length = len(segments)

    def __repr__(self) -> str:
        """
        :return: A detailed representation of the GraphPath.
        """
        return f"GraphPath<length={self.length}>"

    def __len__(self) -> int:
        return self.length


class IRI:
    """
    Represents an IRI.

    :ivar iri: The IRI.
    :vartype iri: str
    """

    def __init__(self, iri: str):
        self.iri = iri

    def __str__(self):
        return self.iri

    def __repr__(self):
        """
        :return: A detailed representation of the IRI.
        """
        return f"IRI<{str(self)}>"


class StringLang:
    """
    Represents a string with a language tag.

    :ivar str: The string.
    :vartype str: str
    :ivar lang: The language tag.
    :vartype lang: str
    """

    def __init__(self, str_: str, lang: str):
        self.str = str_
        self.lang = lang

    def __str__(self):
        return f'"{self.str}"@{self.lang}'

    def __repr__(self):
        """
        :return: A detailed representation of the StringLang.
        """
        return f"StringLang<{str(self)}>"


class StringDatatype:
    """
    Represents a string with a datatype.

    :ivar str: The string.
    :vartype str: str
    :ivar datatype: The IRI of the datatype.
    :vartype datatype: IRI
    """

    def __init__(self, str_: str, datatype: str):
        self.str = str_
        self.datatype = IRI(datatype)

    def __str__(self):
        return f'"{self.str}"^^<{str(self.datatype)}>'

    def __repr__(self):
        """
        :return: A detailed representation of the StringDatatype.
        """
        return f"StringDatatype<{str(self)}>"
