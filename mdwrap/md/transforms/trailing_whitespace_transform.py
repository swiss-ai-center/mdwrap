from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.md.line_context import LineContext


class TrailingWhitespaceTransform(AbstractTransform):
    """Class inmplementing removing trailing whitespaces."""

    def apply(self, *, context: LineContext) -> None:
        """Transform the lines of text."""
        context.current_line.value = context.current_line.value.rstrip()
