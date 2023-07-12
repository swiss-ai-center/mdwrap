from abc import ABC, abstractmethod
from typing import List, Optional, Union

from mdwrap.common.line import Line


class AbstractLineContext(ABC):
    """Class for providing context to a Transform class."""

    def __init__(self) -> None:
        self._lines: List[Line] = []
        self._index = -1

    def set_lines(self, lines: Union[List[str], List[Line]]) -> None:
        """Set the lines of text and reset the class."""
        if all(isinstance(line, str) for line in lines):
            # flake8: noqa
            lines = list(map(lambda l: Line(l), lines))  # type: ignore
        self._lines = lines  # type: ignore
        self._index = -1

    def _check_access(self) -> None:
        """Helper method to check if the lines have been set."""
        if self._index == -1 and not self._lines:
            raise ValueError("Lines must be set before access. Use set_lines().")

    @abstractmethod
    def step(self) -> Optional[Line]:
        """Step to the next line of text."""
        self._check_access()
        if not self._lines and self.index != 0:
            raise ValueError(
                (
                    "Lines are pulluted by previous iteration. "
                    "Use set_lines() to reset."
                )
            )

        self._index += 1
        if self._index < len(self._lines):
            return self.current_line
        return None

    def get_str_lines(self) -> List[str]:
        """Return the lines of text as a list of strings."""
        self._check_access()
        return list(map(lambda l: l.value, self._lines))

    @property
    def lines(self) -> List[Line]:
        """Return the lines of text."""
        self._check_access()
        return self._lines

    @property
    def current_line(self) -> Line:
        """Return the current line of text."""
        self._check_access()
        return self._lines[self._index]

    @property
    def index(self) -> int:
        """Return the current index of the line."""
        self._check_access()
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        """Set the current index of the line."""
        self._check_access()
        self._index = index
