import re
from typing import List


class RegexBuilder:
    """Static Class for building regex expressions."""

    def __init__(self) -> None:  # noqa: D107
        raise ValueError("RegexBuilder is a static class and cannot be instantiated.")

    @staticmethod
    def compile(expressions: List[str]) -> re.Pattern[str]:
        """Compile a list of regex expressions into a single regex."""
        wrapped_expressions = [
            RegexBuilder.wrap_capture_group(expression) for expression in expressions
        ]
        return re.compile("|".join(wrapped_expressions))

    @staticmethod
    def wrap_capture_group(regex: str):
        """Wrap a regex expression in a capture group."""
        return f"(?:{regex})"
