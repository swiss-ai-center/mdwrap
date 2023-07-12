from typing import List, Optional

from mdwrap.common.abstract.abstract_line_context import AbstractLineContext
from mdwrap.common.line import Line
from mdwrap.md.line_context_state import LineContextState


class LineContext(AbstractLineContext):
    """Class for providing context to a Transform class."""

    def __init__(self) -> None:
        """Initialize the line context and reset the state."""
        super().__init__()
        self._state: Optional[LineContextState] = None
        self._state_stack: List[LineContextState] = [LineContextState.AT_ROOT]

    def set_lines(self, lines: List[str] | List[Line]) -> None:
        """Set the lines of text and reset the state."""
        super().set_lines(lines)
        self._state = None
        self._state_stack = [LineContextState.AT_ROOT]

    def _update_state(self, new_state: LineContextState) -> None:
        """Update the state stack."""
        if self._state_stack[-1] == new_state:
            self._state_stack.pop()
        else:
            self._state_stack.append(new_state)

    def step(self) -> Optional[Line]:
        """Return an iterator over the lines of text while updating the index."""
        step = super().step()
        if step is None:
            return None
        line = self.current_line
        line_strip = line.value.strip()
        if line_strip.startswith("```"):
            self._update_state(LineContextState.IN_MULTI_LINE_CODE_BLOCK)
        elif line_strip.startswith("---") and self._state_stack[-1] in [
            LineContextState.AT_ROOT,
            LineContextState.IN_FONT_MATTER,
        ]:
            self._update_state(LineContextState.IN_FONT_MATTER)
        elif line_strip.startswith("|") and line_strip.endswith("|"):
            self._state = LineContextState.IN_TABLE
        else:
            self._state = None
        return line

    @property
    def state(self) -> LineContextState:
        """Return the current state of the line context."""
        return self._state or self._state_stack[-1]
