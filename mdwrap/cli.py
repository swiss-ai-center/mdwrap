import argparse
import re
from pathlib import Path
from typing import List

import pkg_resources

from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.common.formatter import Formatter
from mdwrap.md.line_context import LineContext
from mdwrap.md.transforms.newline_transform import NewlineTransform
from mdwrap.md.transforms.trailing_whitespace_transform import (
    TrailingWhitespaceTransform,
)
from mdwrap.md.transforms.unwrap_transform import UnwrapTransform
from mdwrap.md.transforms.wrap_transform import WrapTransform
from mdwrap.utils.argparse import make_wide


def cli() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="A python based markdown line wrapper",
        formatter_class=make_wide(argparse.ArgumentDefaultsHelpFormatter),
    )
    parser.add_argument(
        "--print-width",
        type=int,
        default=80,
        help="Maximum width of a line",
    )
    parser.add_argument(
        "--fmt",
        action="store_true",
        help="Format files",
    )
    parser.add_argument(
        "--unwrap",
        action="store_true",
        help="Unwrap files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if files are formatted",
    )
    # argparse ignore pattern
    parser.add_argument(
        "--ignore",
        "-i",
        type=str,
        default=(
            r"(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.pytest_cache|\.nox|\.tox|"
            r"\.venv|venv|\.svn|_build|buck-out|build|dist|__pypackages__)"
        ),
        help="Ignore files matching this glob pattern",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s " + pkg_resources.get_distribution("mdwrap").version,
    )
    # List of files or folders
    parser.add_argument(
        "targets", nargs="+", type=str, help="Files or folders of files to format"
    )

    args = parser.parse_args()
    targets = [Path(t) for t in args.targets]
    ignore = args.ignore
    print_width = args.print_width
    fmt = args.fmt
    unwrap = args.unwrap
    check = args.check

    transforms: List[AbstractTransform] = [UnwrapTransform()]

    if not unwrap:
        transforms.append(WrapTransform(print_width=print_width))
    if fmt:
        transforms.extend([NewlineTransform(), TrailingWhitespaceTransform()])

    files: List[Path] = []
    # add files excluding ignored files
    for target in targets:
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(target.glob("**/*.md"))
    if ignore:
        files = [f for f in files if not re.search(ignore, str(f))]

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
                    "(hint: run 'mdwrap [targets ...]' to format them)"
                )
            )
            exit(1)
        else:
            print("SUCCESS: Checks passed. All files are formatted.")
    else:
        for file in files:
            changes = formatter.format(file)
            formatter.log_format_msg(file, changes)
