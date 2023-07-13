import argparse
import importlib.metadata
import re
import warnings
from pathlib import Path
from typing import List

from mdwrap.common.abstract.abstract_transform import AbstractTransform
from mdwrap.md.transforms.newline_transform import NewlineTransform
from mdwrap.md.transforms.trailing_whitespace_transform import (
    TrailingWhitespaceTransform,
)
from mdwrap.md.transforms.unwrap_transform import UnwrapTransform
from mdwrap.md.transforms.wrap_transform import WrapTransform


class MDWrapArgparse(argparse.ArgumentParser):
    """Argument parser for mdwrap."""

    def __init__(self):
        """Initialize the argument parser."""
        super().__init__(
            description="A python based markdown line wrapper",
            formatter_class=MDWrapArgparse.make_wide(
                argparse.ArgumentDefaultsHelpFormatter
            ),
        )
        self.add_argument(
            "--print-width",
            type=int,
            default=80,
            help="Maximum width of a line",
        )
        self.add_argument(
            "--fmt",
            action="store_true",
            help="Format files",
        )
        self.add_argument(
            "--unwrap",
            action="store_true",
            help="Unwrap files",
        )
        self.add_argument(
            "--check",
            action="store_true",
            help="Check if files are formatted",
        )
        self.add_argument(
            "--ignore",
            "-i",
            type=str,
            default=(
                # Ingore pattern extended from black (https://github.com/psf/black)
                r"\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.pytest_cache|\.nox|\.tox|"
                r"\.venv|venv|\.svn|_build|buck-out|build|dist|__pypackages__"
            ),
            help="Ignore files matching this glob pattern",
        )
        self.add_argument(
            "--ignore-extend",
            "-I",
            type=str,
            default=None,
            help="Extend the default ignore pattern with this glob pattern",
        )
        self.add_argument(
            "--version",
            "-v",
            action="version",
            version="%(prog)s " + importlib.metadata.version("mdwrap"),
        )
        # List of files or folders
        self.add_argument(
            "targets", nargs="+", type=str, help="Files or folders of files to format"
        )

    def parse_args(self, args=None, namespace=None):
        """Parse arguments and return a tuple of (args, files, transforms)."""
        args = super().parse_args(args=args, namespace=namespace)
        targets = [Path(t) for t in args.targets]

        transforms: List[AbstractTransform] = [UnwrapTransform()]

        if not args.unwrap:
            transforms.append(WrapTransform(print_width=args.print_width))
        if args.fmt:
            transforms.extend([NewlineTransform(), TrailingWhitespaceTransform()])

        files: List[Path] = []
        for target in targets:
            if target.is_file() and target.suffix == ".md":
                files.append(target)
            elif target.is_dir():
                files.extend(target.glob("**/*.md"))
        ignore_pattern = None
        if args.ignore_extend:
            ignore_pattern = args.ignore + "|" + args.ignore_extend
        else:
            ignore_pattern = args.ignore
        files = [f for f in files if not re.match(ignore_pattern, str(f))]
        return args, files, transforms

    @staticmethod
    def make_wide(formatter, w=80, h=36):
        """Return a wider HelpFormatter, if possible."""
        try:
            # https://stackoverflow.com/a/5464440
            # beware: "Only the name of this class is considered a public API."
            kwargs = {'width': w, 'max_help_position': h}
            formatter(None, **kwargs)
            return lambda prog: formatter(prog, **kwargs)
        except TypeError:
            warnings.warn("argparse help formatter failed, falling back.")  # noqa: B028
            return formatter
