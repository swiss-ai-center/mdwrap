from dataclasses import dataclass
from typing import List

from mdwrap.classes.regex_builder import RegexBuilder


@dataclass
class MDTokenizer:
    """Class for tokenizing markdown text into a list of tokens."""

    TOKENS_REGEX = RegexBuilder.compile(
        [
            r"(?:[^\s]+)?!?\[.*?\]\(.*?\)(?:[^\s]+)?",  # images
            r"(?:[^\s]+)?\[.*?\]\(.*?\)(?:[^\s]+)?",  # markdown links
            r"(?:[^\s\*]+)?\*\*.*?\*\*+(?:[^\s\*]+)?",  # bold
            r"(?:[^\s_]+)?__.*?__+(?:[^\s_]+)?",  # bold
            r"(?:[^\s`]+)?`.*?`(?:[^\s`]+)?",  # code
            r"(?:[^\s\*]+)?\*.*?\*(?:[^\s\*]+)?",  # italic
            r"(?:[^\s_]+)?_.*?_(?:[^\s_]+)?",  # italic
            r"[^\s]+",  # text
        ]
    )

    def tokenize(self, text: str) -> List[str]:
        """Tokenize markdown text into a list of tokens."""
        tokens = []
        for match in self.TOKENS_REGEX.finditer(text):
            tokens.append(match.group(0))
        return tokens
