import re
from pathlib import Path

from mdwrap.utils.argparse import MDWrapArgparse


def test_parse_args():
    """Test parsing arguments."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = [
        "--print-width",
        "100",
        "--fmt",
        "--unwrap",
        "--check",
        "--ignore",
        ".git",
        "--ignore-extend",
        ".git",
        "tests/integration/paragraph",
    ]

    # Parse the arguments
    args, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert args.print_width == 100
    assert args.fmt is True
    assert args.unwrap is True
    assert args.check is True
    assert args.ignore == ".git"
    assert args.ignore_extend == ".git"

    assert files == [
        Path('tests/integration/paragraph/expected.md'),
        Path('tests/integration/paragraph/test.md'),
    ]
    assert len(transforms) > 0


def test_parse_args_with_default_values():
    """Test parsing arguments with default values."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = ["file.md"]

    # Parse the arguments
    args, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert args.print_width == 80
    assert args.fmt is False
    assert args.unwrap is False
    assert args.check is False
    assert args.ignore == (
        r"\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.pytest_cache|\.nox|\.tox|"
        r"\.venv|venv|\.svn|_build|buck-out|build|dist|__pypackages__"
    )
    assert args.ignore_extend is None

    # Empty because file.md does not exist
    assert files == []
    assert len(transforms) > 0


def test_parse_args_with_ignore_pattern():
    """Test parsing arguments with ignore pattern."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = ["--ignore", "README.md", "."]

    # Parse the arguments
    args, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert args.ignore == "README.md"

    assert all(re.match(args.ignore, str(f)) for f in files) is False
    assert len(transforms) > 0


def test_parse_args_with_ignore_extend():
    """Test parsing arguments with ignore extend."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = ["--ignore-extend", "README.md", "."]

    # Parse the arguments
    args, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert args.ignore_extend == "README.md"

    assert all(re.match(args.ignore_extend, str(f)) for f in files) is False
    assert len(transforms) > 0


def test_parse_args_with_mutiple_targets():
    """Test parsing arguments with multiple targets."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = ["tests/integration/paragraph", "tests/integration/list"]

    # Parse the arguments
    _, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert files == [
        Path('tests/integration/paragraph/expected.md'),
        Path('tests/integration/paragraph/test.md'),
        Path('tests/integration/list/expected.md'),
        Path('tests/integration/list/test.md'),
    ]
    assert len(transforms) > 0


def test_parse_args_with_mutiple_targets_and_ignore():
    """Test parsing arguments with multiple targets and ignore."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = [
        "--ignore",
        "tests/integration/paragraph",
        "tests/integration/paragraph",
        "tests/integration/list",
    ]

    # Parse the arguments
    _, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert files == [
        Path('tests/integration/list/expected.md'),
        Path('tests/integration/list/test.md'),
    ]
    assert len(transforms) > 0


def test_parse_args_with_mutiple_targets_and_ignore_extend():
    """Test parsing arguments with multiple targets and ignore."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = [
        "--ignore-extend",
        "tests/integration/paragraph",
        "tests/integration/paragraph",
        "tests/integration/list",
    ]

    # Parse the arguments
    _, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert files == [
        Path('tests/integration/list/expected.md'),
        Path('tests/integration/list/test.md'),
    ]
    assert len(transforms) > 0


def test_parse_args_only_md_files():
    """Test parsing arguments with only md files."""
    parser = MDWrapArgparse()

    # Prepare test arguments
    test_args = ["pyproject.toml", "tests/integration/paragraph/test.md"]

    # Parse the arguments
    _, files, transforms = parser.parse_args(test_args)

    # Assertions
    assert files == [
        Path('tests/integration/paragraph/test.md'),
    ]
    assert len(transforms) > 0
