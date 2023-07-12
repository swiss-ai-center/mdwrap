from typing import List

import pytest

from mdwrap.md.line_context import LineContext
from mdwrap.md.transforms.unwrap_transform import UnwrapTransform


def test_apply() -> None:
    """Test apply method."""
    line_context = LineContext()
    transform = UnwrapTransform()
    line_context.set_lines(["Hello", "World"])
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == ["Hello World"]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["  Hello", "  World"], ["  Hello World"]),
        (["  Hello", "    World"], ["  Hello", "    World"]),
        (["- Hello", "  - World"], ["- Hello", "  - World"]),
        (["- Hello", "  World"], ["- Hello World"]),
        (["* Hello", "  World"], ["* Hello World"]),
        (["+ Hello", "  World"], ["+ Hello World"]),
        (["1. Hello", "   World"], ["1. Hello World"]),
        (["10. Hello", "    World"], ["10. Hello World"]),
        (["- [ ] Hello", "      World"], ["- [ ] Hello World"]),
        (["- [x] Hello", "      World"], ["- [x] Hello World"]),
        (["- [X] Hello", "      World"], ["- [X] Hello World"]),
    ],
)
def test_apply_with_indent(test_input: List[str], expected: List[str]) -> None:
    """Test apply method with indent."""
    line_context = LineContext()
    transform = UnwrapTransform()
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["Hello ", "World"], ["Hello World"]),
        (["Hello  ", "World"], ["Hello World"]),
    ],
)
def test_apply_with_trailing_whitespace(
    test_input: List[str], expected: List[str]
) -> None:
    """Test apply method with indent."""
    line_context = LineContext()
    transform = UnwrapTransform()
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["- Hello", "- World"], ["- Hello", "- World"]),
        (["* Hello", "* World"], ["* Hello", "* World"]),
        (["+ Hello", "+ World"], ["+ Hello", "+ World"]),
        (["1. Hello", "2. World"], ["1. Hello", "2. World"]),
        (["10. Hello", "11. World"], ["10. Hello", "11. World"]),
        (["- [ ] Hello", "- [ ] World"], ["- [ ] Hello", "- [ ] World"]),
        (["- [x] Hello", "- [x] World"], ["- [x] Hello", "- [x] World"]),
        (["- [X] Hello", "- [X] World"], ["- [X] Hello", "- [X] World"]),
        (["# Hello", "World"], ["# Hello", "World"]),
        (["> Hello", "World"], ["> Hello", "World"]),
        (["=== Hello", "World"], ["=== Hello", "World"]),
        (["??? Hello", "World"], ["??? Hello", "World"]),
        (["[//]: Hello", "World"], ["[//]: Hello", "World"]),
    ],
)
def test_apply_with_non_wrappable(test_input: List[str], expected: List[str]) -> None:
    """Test apply method with non wrappable types."""
    line_context = LineContext()
    transform = UnwrapTransform()
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected
