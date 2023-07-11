from mdwrap.md.tokenizer import Tokenizer


def cli() -> None:
    """Main cli function."""
    tokenizer = Tokenizer()
    print(tokenizer.TOKENS_REGEX)
    tokens = tokenizer.tokenize("Hello **world**, **_im here_**")
    print(tokens)
