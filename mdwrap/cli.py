from mdwrap.common.formatter import Formatter
from mdwrap.md.line_context import LineContext
from mdwrap.utils.argparse import MDWrapArgparse


def cli() -> None:
    """CLI entrypoint."""
    args, files, transforms = MDWrapArgparse().parse_args()

    line_context = LineContext()
    formatter = Formatter(
        line_context=line_context,
        transforms=transforms,
    )

    if args.check:
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
