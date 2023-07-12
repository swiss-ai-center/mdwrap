from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.md.line_context import LineContext
from mdwrap.md.line_context_state import LineContextState


class NewlineTransform(AbstractTransform):
    """Class inmplementing merging newlines."""

    def apply(self, *, context: LineContext) -> None:
        """Transform the lines of text."""
        line = context.current_line
        index = context.index
        next_line = context.lines[index + 1] if index + 1 < len(context.lines) else None
        apply_condition = (
            # Current line checks
            context.state == LineContextState.AT_ROOT
            and line.value.strip() == ""
            and next_line
            and next_line.value.strip() == ""
        )
        if apply_condition:
            # Delete the line
            context.lines.pop(index)
            context.index -= 1
