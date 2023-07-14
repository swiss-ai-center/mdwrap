import re
from typing import List, Optional

from mdwrap.common.abstract.abstract_line_context import AbstractLineContext
from mdwrap.common.line import Line
from mdwrap.md.line_context_state import LineContextState
from mdwrap.md.regex import Regex


class LineContext(AbstractLineContext):
    """Class for providing context to a Transform class."""

    STATE_REGEXES = {
        LineContextState.IN_HTML: Regex.IN_HTML,
        LineContextState.IN_MULTI_LINE_CODE_BLOCK: Regex.IN_MULTI_LINE_CODE_BLOCK,
        LineContextState.IN_MULTI_LINE_MATH_BLOCK: Regex.IN_MULTI_LINE_MATH_BLOCK,
        LineContextState.IN_FRONT_MATTER: Regex.IN_FRONT_MATTER,
    }

    def __init__(self) -> None:
        """Initialize the line context and reset the state."""
        super().__init__()
        self._state: List[LineContextState] = []
        self._last_lines_len = 0

    def set_lines(self, lines: List[str] | List[Line]) -> None:
        """Set the lines of text and reset the state."""
        super().set_lines(lines)
        self._last_lines_len = len(self._lines)
        self._compute_state()

    def _compute_state(self) -> None:
        """Compute the state of each line of text."""
        content = "\n".join([line.value.strip() for line in self._lines])

        self._state = [LineContextState.AT_ROOT for _ in range(len(self._lines))]

        # Set self._state line index to regex match
        for state, regex in self.STATE_REGEXES.items():
            for match in re.finditer(regex.value, content, re.MULTILINE):
                # Convert match start and end to line index
                start = content[: match.start()].count("\n")
                end = content[: match.end()].count("\n")
                for i in range(start, end):
                    self._state[i] = state

    def step(self) -> Optional[Line]:
        """Return an iterator over the lines of text while updating the index."""
        step = super().step()
        if step is None:
            return None

        if len(self._lines) != self._last_lines_len:
            nb_lines_added = len(self._lines) - self._last_lines_len
            if nb_lines_added > 0:
                for i in range(nb_lines_added):
                    self._state.insert(self.index + i, LineContextState.AT_ROOT)
            else:
                for _ in range(-nb_lines_added):
                    self._state.pop(self.index)
        self._last_lines_len = len(self._lines)
        return self.current_line

    @property
    def state(self) -> LineContextState:
        """Return the current state of the line context."""
        return self._state[self.index]

    @property
    def state_next(self) -> LineContextState:
        """Return the current state of the line context."""
        if self.index + 1 >= len(self._state):
            return LineContextState.AT_ROOT
        return self._state[self.index + 1]
