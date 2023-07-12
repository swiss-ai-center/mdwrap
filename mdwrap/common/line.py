from typing import Optional


class Line:
    """Class representing a line of text."""

    def __init__(self, line: str, *, indent_width: Optional[int] = None) -> None:
        """Initialize the line.

        Args:
            line: The text value of the line.
            indent_width: The width of the indent.
        """
        if indent_width:
            line = " " * indent_width + line.lstrip()
        self.setup(line)

    def setup(self, line: str) -> None:
        """Set up the line."""
        self._line = line
        self._indent_width = len(line) - len(line.lstrip())

    @property
    def value(self) -> str:
        """Return the text value of the line."""
        return self._line

    @value.setter
    def value(self, line: str) -> None:
        """Set the text value of the line."""
        self.setup(line)

    @property
    def indent_width(self) -> int:
        """Return the width of the indent."""
        return self._indent_width

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return NotImplemented
        return self._line == other._line

    def __hash__(self) -> int:
        return hash(self._line)

    def __str__(self) -> str:
        return self._line

    def __repr__(self) -> str:
        return f"Line(line={self._line!r})"

    def copy(self) -> "Line":
        """Return a copy of the line."""
        return Line(self._line, indent_width=self._indent_width)
