from typing import List
import re


class RegexBuilder:
    @staticmethod
    def compile(expressions: List[str]) -> str:
        """Compile a list of regex expressions into a single regex."""
        wrapped_expressions = [
            RegexBuilder.wrap_capture_group(expression) for expression in expressions
        ]
        return re.compile("|".join(wrapped_expressions))

    @staticmethod
    def wrap_capture_group(regex: str):
        """Wrap a regex expression in a capture group."""
        return f"(?:{regex})"
