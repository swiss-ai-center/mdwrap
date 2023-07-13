import re

from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.md.line_context import LineContext
from mdwrap.md.line_context_state import LineContextState
from mdwrap.md.regex import Regex


class UnwrapTransform(AbstractTransform):
    """Class inmplementing unwrapping a line of text."""

    def apply(self, *, context: LineContext) -> None:
        """Transform the lines of text."""
        line = context.current_line
        index = context.index
        next_line = context.lines[index + 1] if index + 1 < len(context.lines) else None
        list_match_line = re.match(Regex.LIST_START.value, line.value.lstrip())
        apply_condition = (
            # Current line checks
            context.state == LineContextState.AT_ROOT
            and line.value.strip() != ""
            and not re.match(Regex.IGNORE_START.value, line.value.lstrip())
            # Next line checks
            and next_line
            and next_line.value.strip() != ""
            and (
                # List indent condition
                next_line.indent_width == line.indent_width
                or (list_match_line and next_line.indent_width == list_match_line.end())
            )
            and not re.match(Regex.IGNORE_START.value, next_line.value.lstrip())
            and not re.match(Regex.LIST_START.value, next_line.value.lstrip())
            and not re.match(Regex.HTML_OPEN_TAG.value, next_line.value.lstrip())
        )
        if apply_condition:
            # Merge the lines
            line.value = (
                line.value.rstrip() + " " + next_line.value.lstrip()  # type: ignore
            )
            context.lines.pop(index + 1)
            context.index -= 1
