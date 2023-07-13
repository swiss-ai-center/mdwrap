from typing import List

from mdwrap.md.regex import Regex
from mdwrap.utils.regex_builder import RegexBuilder


class Tokenizer:
    """Class for tokenizing markdown text into a list of tokens."""

    TOKENS_REGEX = RegexBuilder.compile(
        [
            Regex.LIST_START.value,
            Regex.IMAGE.value,
            Regex.LINK.value,
            Regex.INLINE_CODE.value,
            Regex.INLINE_MATH.value,
            Regex.HIGHLIGH_TEXT.value,
            Regex.UNDERLINE_TEXT.value,
            Regex.STRIKETHROUGH_TEXT.value,
            Regex.BOLD_TEXT1.value,
            Regex.BOLD_TEXT2.value,
            Regex.ITALIC_TEXT1.value,
            Regex.ITALIC_TEXT2.value,
            Regex.KEYBOARD_KEYS_TEXT.value,
            Regex.WORD.value,
        ]
    )

    def tokenize(self, text: str) -> List[str]:
        """Tokenize markdown text into a list of tokens."""
        tokens = []
        for match in self.TOKENS_REGEX.finditer(text):
            tokens.append(match.group(0).strip())
        return tokens
