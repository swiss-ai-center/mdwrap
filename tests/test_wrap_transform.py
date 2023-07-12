from typing import List

import pytest

from mdwrap.md.line_context import LineContext
from mdwrap.md.transforms.wrap_transform import WrapTransform


def test_apply() -> None:
    """Test apply method."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(["Hello World"])
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == ["Hello", "World"]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["Hello here"], ["Hello here"]),
        (["Hello here!"], ["Hello", "here!"]),
    ],
)
def test_apply_max_print_width(test_input: List[str], expected: List[str]) -> None:
    """Test apply method at max print width."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["  Hello World"], ["  Hello", "  World"]),
    ],
)
def test_apply_with_indent(test_input: List[str], expected: List[str]) -> None:
    """Test apply method with indent."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["  Hello  World"], ["  Hello", "  World"]),
        (["  Hello  World  "], ["  Hello", "  World"]),
    ],
)
def test_apply_with_trailing_whitespace(
    test_input: List[str], expected: List[str]
) -> None:
    """Test apply method with trailing whitespace."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["- Hello - World"], ["- Hello -", "  World"]),
        (["* Hello * World"], ["* Hello *", "  World"]),
        (["+ Hello + World"], ["+ Hello +", "  World"]),
        (["1. Hello 2. World"], ["1. Hello 2.", "   World"]),
        (["10. Hello 11. World"], ["10. Hello 11.", "    World"]),
        (["- [ ] Hello - [ ] World"], ["- [ ] Hello -", "      [ ] World"]),
        (["- [x] Hello - [x] World"], ["- [x] Hello -", "      [x] World"]),
        (["- [X] Hello - [X] World"], ["- [X] Hello -", "      [X] World"]),
    ],
)
def test_apply_with_lists(test_input: List[str], expected: List[str]) -> None:
    """Test apply method on lists."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["# Hello World"], ["# Hello World"]),
        (["> Hello World"], ["> Hello World"]),
        (["> Hello > World"], ["> Hello > World"]),
        (["=== Hello World"], ["=== Hello World"]),
        (["??? Hello World"], ["??? Hello World"]),
        (["[//]: Hello World"], ["[//]: Hello World"]),
    ],
)
def test_apply_with_non_wrappable(test_input: List[str], expected: List[str]) -> None:
    """Test apply method with non wrappable types."""
    line_context = LineContext()
    transform = WrapTransform(print_width=10)
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected
