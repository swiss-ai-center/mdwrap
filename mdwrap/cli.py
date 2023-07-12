import argparse
from pathlib import Path
from typing import List

from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.common.formatter import Formatter
from mdwrap.md.line_context import LineContext
from mdwrap.md.newline_transform import NewlineTransform
from mdwrap.md.unwrap_transform import UnwrapTransform
from mdwrap.md.wrap_transform import WrapTransform


def cli() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--print-width",
        type=int,
        default=80,
        help="Maximum width of a line",
    )
    parser.add_argument(
        "--fmt",
        action="store_true",
        help="Format the file(s) (basic newline formatting)",
    )
    parser.add_argument(
        "--unwrap",
        action="store_true",
        help="Unwrap the file(s)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the file(s) is/are formatted",
    )
    parser.add_argument("target", help="File or folder of files to format")

    args = parser.parse_args()
    target = Path(args.target)
    print_width = args.print_width
    fmt = args.fmt
    unwrap = args.unwrap
    check = args.check

    transforms: List[AbstractTransform] = [UnwrapTransform()]

    if not unwrap:
        transforms.append(WrapTransform(print_width=print_width))
    if fmt:
        transforms.append(NewlineTransform())

    files = [target] if target.is_file() else list(target.glob("**/*.md"))
    line_context = LineContext()
    formatter = Formatter(
        line_context=line_context,
        transforms=transforms,
    )
    if check:
        print("Checking files...")
        failed = False
        for file in files:
            if not formatter.check(file):
                print(file)
                failed = True
        if failed:
            print(
                (
                    "ERROR: Checks failed. The files above are not formatted. "
                    "(run mdwrap to format them)"
                )
            )
            exit(1)
        else:
            print("SUCCESS: Checks passed. All files are formatted.")
    else:
        for file in files:
            changes = formatter.format(file)
            formatter.log_format_msg(file, changes)
