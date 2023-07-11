from mdwrap.classes.md_tokenizer import MDTokenizer


def cli() -> None:
    """Main cli function."""
    tokenizer = MDTokenizer()
    print(tokenizer.TOKENS_REGEX)
    tokens = tokenizer.tokenize("Hello **world**, **_im here_**")
    print(tokens)
