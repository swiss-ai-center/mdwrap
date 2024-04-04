import re
from typing import List, Optional, Union

from mdwrap.common.abstract.abstract_line_context import AbstractLineContext
from mdwrap.common.line import Line
from mdwrap.md.line_context_state import LineContextState
from mdwrap.md.regex import Regex
from mdwrap.utils.regex_builder import RegexBuilder


class LineContext(AbstractLineContext):
    """Class for providing context to a Transform class."""

    SWITCH_STATE_REGEXES = {
        LineContextState.IN_MULTI_LINE_CODE_BLOCK: Regex.MULTI_LINE_CODE_BLOCK_START,
        LineContextState.IN_MULTI_LINE_MATH_BLOCK: Regex.MULTI_LINE_MATH_BLOCK_START,
        LineContextState.IN_FRONT_MATTER: Regex.FRONT_MATTER_START,
    }
    HTML_TAG_REGEX = RegexBuilder.compile(
        [Regex.HTML_OPEN_TAG.value, Regex.HTML_CLOSE_TAG.value]
    )

    def __init__(self) -> None:
        """Initialize the line context and reset the state."""
        super().__init__()
        self._state_stack: List[LineContextState] = [LineContextState.AT_ROOT]

    def set_lines(self, lines: Union[List[str], List[Line]]) -> None:
        """Set the lines of text and reset the state."""
        super().set_lines(lines)
        self._state_stack = [LineContextState.AT_ROOT]

    def _switch_state(self, target_state: LineContextState) -> None:
        """Update the state as a switch."""
        if self._state_stack[-1] == target_state:
            self._state_stack.pop()
        else:
            self._state_stack.append(target_state)

    def step(self) -> Optional[Line]:
        """Return an iterator over the lines of text while updating the index."""
        step = super().step()
        if step is None:
            return None

        line_strip = self.current_line.value.strip()
        # Exit early for comments
        if re.match(Regex.HTML_COMMENT.value, line_strip) is not None:
            return self.current_line
        # Update the state
        if self.state in [
            LineContextState.AT_ROOT,
            LineContextState.IN_HTML,
        ]:
            if matches := list(re.finditer(self.HTML_TAG_REGEX, line_strip)):
                for match in matches:
                    if re.match(Regex.HTML_OPEN_TAG.value, match.group()):
                        self._state_stack.append(LineContextState.IN_HTML)
                    elif (
                        re.match(Regex.HTML_CLOSE_TAG.value, match.group())
                        and self._state_stack[-1] == LineContextState.IN_HTML
                    ):
                        self._state_stack.pop()

        for state, regex in self.SWITCH_STATE_REGEXES.items():
            if re.match(regex.value, line_strip) and self._state_stack[-1] in [
                LineContextState.AT_ROOT,
                state,
            ]:
                self._switch_state(state)
                break
        return self.current_line

    @property
    def state(self) -> LineContextState:
        """Return the current state of the line context."""
        return self._state_stack[-1]
