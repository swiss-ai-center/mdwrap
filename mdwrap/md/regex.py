from enum import Enum


class Regex(Enum):
    """Regex for markdown and Material for MkDocs."""

    IGNORE_START = r"^#+ |^=== |^\?\?\? |^> |\[\/\/\]: "
    LIST_START = r"^(-|\*|\+|\d+\.)( +\[[ xX]\])? +"

    IMAGE = r"(?:[^\s]+)?!?\[.*?\]\(.*?\)(?:[^\s]+)?"
    LINK = r"(?:[^\s]+)?\[.*?\]\(.*?\)(?:[^\s]+)?"
    INLINE_CODE = r"(?:[^\s`]+)?`.*?`(?:[^\s`]+)?"
    BOLD_TEXT1 = r"(?:[^\s]+)?\*\*[^\s\*(_\s)][^\*]*?[^\s\*(_\s)]\*\*(?:[^\s]+)?"
    BOLD_TEXT2 = r"(?:[^\s]+)?__[^\s_(\*\s)][^_]*?[^\s_(\*\s)]__(?:[^\s]+)?"
    ITALIC_TEXT1 = r"(?:[^\s\*]+)?\*[^\s\*(_\s)][^\*]*?[^\s\*(_\s)]\*(?:[^\s\*]+)?"
    ITALIC_TEXT2 = r"(?:[^\s_]+)?_[^\s_(\*\s)][^_]*?[^\s_(\*\s)]_(?:[^\s_]+)?"
    WORD = r"[^\s]+"
