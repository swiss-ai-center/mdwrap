from typing import List

import pytest

from mdwrap.md.line_context import LineContext
from mdwrap.md.transforms.trailing_whitespace_transform import (
    TrailingWhitespaceTransform,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["Hello world"], ["Hello world"]),
        (["Hello world  "], ["Hello world"]),
    ],
)
def test_apply(test_input: List[str], expected: List[str]) -> None:
    """Test apply method."""
    line_context = LineContext()
    transform = TrailingWhitespaceTransform()
    line_context.set_lines(test_input)
    while line_context.step():
        transform.apply(context=line_context)
    assert line_context.get_str_lines() == expected
