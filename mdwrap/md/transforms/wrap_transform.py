import re

from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.common.line import Line
from mdwrap.md.line_context import LineContext
from mdwrap.md.line_context_state import LineContextState
from mdwrap.md.regex import Regex
from mdwrap.md.tokenizer import Tokenizer


class WrapTransform(AbstractTransform):
    """Class inmplementing wrapping a line of text."""

    def __init__(self, *, print_width: int) -> None:
        """Initialize the wrap transform.

        Args:
            print_width: The width to wrap the text at.
        """
        super().__init__()
        self._tokenizer = Tokenizer()
        self._print_width = print_width

    def _create_new_line(
        self,
        *,
        context: LineContext,
        value: str,
        in_new_wrapped_line: bool,
        current_line: Line,
    ) -> None:
        """Create a new line."""
        list_indent_width = 0
        if in_new_wrapped_line:
            if match := re.match(Regex.LIST_START.value, current_line.value.lstrip()):
                list_indent_width = match.end()
        line = Line(
            value.rstrip(), indent_width=current_line.indent_width + list_indent_width
        )
        if not in_new_wrapped_line:
            context.lines.pop(context.index)
        else:
            # We only increment the index if we are in a new wrapped line, as we are
            # inserting a new line right after
            context.index += 1
        context.lines.insert(context.index, line)

    def _wrap_line(self, *, context: LineContext) -> None:
        """Wrap the line."""
        current_line = context.current_line.copy()
        new_line = ""
        in_new_wrapped_line = False
        tokens = self._tokenizer.tokenize(context.current_line.value)
        for i, token in enumerate(tokens):
            new_line += token
            is_start_of_list = (
                re.match(Regex.LIST_START.value, (new_line + " ").lstrip()) and i == 0
            )
            is_line_too_long = (
                i + 1 < len(tokens)
                and len(new_line) + len(tokens[i + 1]) + 1 > self._print_width
                # We add 1 for the space between        ^^^
            )
            is_next_token_list_start = i + 1 < len(tokens) and re.match(
                Regex.LIST_START.value, (tokens[i + 1] + " ").lstrip()
            )
            wrap_condition = (
                not is_start_of_list
                and is_line_too_long
                and not is_next_token_list_start
            )
            if wrap_condition:
                self._create_new_line(
                    context=context,
                    value=new_line,
                    in_new_wrapped_line=in_new_wrapped_line,
                    current_line=current_line,
                )
                new_line = ""
                in_new_wrapped_line = True
            else:
                new_line += " "
        if new_line:
            self._create_new_line(
                context=context,
                value=new_line,
                in_new_wrapped_line=in_new_wrapped_line,
                current_line=current_line,
            )

    def apply(self, *, context: LineContext) -> None:
        """Transform the lines of text."""
        line = context.current_line
        apply_condition = (
            # Current line checks
            context.state == LineContextState.AT_ROOT
            and line.value.strip() != ""
            and not re.match(Regex.IGNORE_START.value, line.value.lstrip())
            and not re.match(Regex.HTML_TAG.value, line.value.lstrip())
            and len(line.value) > self._print_width
        )
        if apply_condition:
            # Wrap the lines
            self._wrap_line(context=context)
