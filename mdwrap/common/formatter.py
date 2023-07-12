from pathlib import Path
from typing import List, Union

from mdwrap.common.abstract.abstract_line_context import AbstractLineContext
from mdwrap.common.abstract.abstract_transform import AbstractTransform


class Formatter:
    """Class for formatting a file."""

    def __init__(
        self, *, line_context: AbstractLineContext, transforms: List[AbstractTransform]
    ):
        """Initialize the formatter.

        Args:
            line_context: The line context to use.
            transforms: The transforms to apply.
        """
        self._line_context = line_context
        self._transforms = transforms

    def format(self, file_path: Path) -> bool:
        """Format a file and return if changes occured."""
        text = file_path.read_text()
        formatted = self._format_text(text)
        file_path.write_text(formatted)
        changes = text != formatted
        return changes

    def check(self, file_path: Path) -> bool:
        """Check if a file is formatted."""
        return file_path.read_text() == self._format_text(file_path.read_text())

    def log_format_msg(self, msg: Union[str, Path], changes: bool) -> None:
        """Print normal text if changes occured, else print dark text."""
        if changes:
            print(msg)
        else:
            print(f"\033[90m{msg}\033[0m")

    def _format_text(self, text: str) -> str:
        """Format the text."""
        lines = text.splitlines()
        if not lines:
            return ""
        for transform in self._transforms:
            self._line_context.set_lines(lines)
            while self._line_context.step():
                transform.apply(context=self._line_context)
            lines = self._line_context.get_str_lines()
        return "\n".join(lines) + "\n"
