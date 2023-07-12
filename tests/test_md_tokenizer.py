from typing import List

import pytest

from mdwrap.md.tokenizer import Tokenizer

tokenizer = Tokenizer()

IMAGE_TEMPLATES = ["![{}]()", "![]({})"]
LINK_TEMPLATES = ["[{}]()", "[]({})"]

CODE_TEMPLATES = ["`{}`"]
CODE_BOLD_TEMPLATES = ["`**{}**`", "`__{}__`"]
CODE_ITALIC_TEMPLATES = ["`*{}*`", "`_{}_`"]
CODE_BOLD_ITALIC_TEMPLATES = ["`***{}***`", "`___{}___`", "`**_{}_**`", "`__*{}*__`"]
CODE_ITALIC_BOLD_TEMPLATES = ["`*__{}__*`", "`_**{}**_`"]
BOLD_TEMPLATES = ["**{}**", "__{}__"]
ITALIC_TEMPLATES = ["*{}*", "_{}_"]
BOLD_ITALIC_TEMPLATES = ["***{}***", "___{}___", "**_{}_**", "__*{}*__"]
ITALIC_BOLD_TEMPLATES = ["*__{}__*", "_**{}**_"]

STYLE_TEMPLATES = (
    CODE_TEMPLATES
    + CODE_BOLD_TEMPLATES
    + CODE_ITALIC_TEMPLATES
    + CODE_BOLD_ITALIC_TEMPLATES
    + CODE_ITALIC_BOLD_TEMPLATES
    + BOLD_TEMPLATES
    + ITALIC_TEMPLATES
    + BOLD_ITALIC_TEMPLATES
    + ITALIC_BOLD_TEMPLATES
)

TEMPLATES = IMAGE_TEMPLATES + LINK_TEMPLATES + STYLE_TEMPLATES

PUNCTUATION = [".", ",", "!", "?", ":", ";", "-", "(", ")", "[", "]", "{", "}", "..."]


def _get_test_image_and_link():
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        yield template.format("Hello world")


@pytest.mark.parametrize("test_input", _get_test_image_and_link())
def test_image_and_link(test_input) -> None:
    """Test images and links."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == [test_input]


def _get_test_image_and_link_punctuation():
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for punctuation in PUNCTUATION:
            yield (
                "Hello " + punctuation + template.format("world") + punctuation,
                [
                    "Hello",
                    punctuation + template.format("world") + punctuation,
                ],
            )


@pytest.mark.parametrize("test_input,expected", _get_test_image_and_link_punctuation())
def test_image_and_link_punctuation(test_input: str, expected: List[str]) -> None:
    """Test punctuation included in images and links."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == expected


def _get_test_image_and_link_multiple():
    for template1 in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for template2 in IMAGE_TEMPLATES + LINK_TEMPLATES:
            yield template1.format("Hello") + " " + template2.format("world")


@pytest.mark.parametrize("test_input", _get_test_image_and_link_multiple())
def test_image_and_link_multiple(test_input: str) -> None:
    """Test multiple images and links in the same string."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == test_input.split(" ")


def _get_test_style():
    for template in STYLE_TEMPLATES:
        yield template.format("Hello world")


@pytest.mark.parametrize("test_input", _get_test_style())
def test_style(test_input: str) -> None:
    """Test style."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == [test_input]


def _get_test_style_non_valid():
    for template in (
        BOLD_TEMPLATES
        + ITALIC_TEMPLATES
        + BOLD_ITALIC_TEMPLATES
        + ITALIC_BOLD_TEMPLATES
    ):
        yield template.format(" Hello world ")


@pytest.mark.parametrize("test_input", _get_test_style_non_valid())
def test_style_non_valid(test_input: str) -> None:
    """Test style with non valid characters."""
    tokens = tokenizer.tokenize(test_input)
    assert len(tokens) != 1, tokens


def _get_test_style_punctuation():
    for template in STYLE_TEMPLATES:
        for punctuation in PUNCTUATION:
            yield (
                "Hello " + punctuation + template.format("world") + punctuation,
                [
                    "Hello",
                    punctuation + template.format("world") + punctuation,
                ],
            )


@pytest.mark.parametrize("test_input,expected", _get_test_style_punctuation())
def test_style_punctuation(test_input: str, expected: List[str]) -> None:
    """Test punctuation included in bold and italic."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == expected


def _get_test_style_muliple():
    for template1 in STYLE_TEMPLATES:
        for template2 in STYLE_TEMPLATES:
            yield template1.format("Hello") + " " + template2.format("world")


@pytest.mark.parametrize("test_input", _get_test_style_muliple())
def test_style_muliple(test_input: str) -> None:
    """Test multiple bold and italic in the same string."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == test_input.split()


def _get_test_style_within_image_or_link():
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for style_template in STYLE_TEMPLATES:
            yield template.format(style_template.format("Hello"))


@pytest.mark.parametrize("test_input", _get_test_style_within_image_or_link())
def test_style_within_image_or_link(test_input: str) -> None:
    """Test style within images and links."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == [test_input]


def _get_test_mix():
    for template1 in TEMPLATES:
        for template2 in TEMPLATES:
            yield template1.format("Hello") + " " + template2.format("world")


@pytest.mark.parametrize("test_input", _get_test_mix())
def test_mix(test_input: str) -> None:
    """Test mixing all templates."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == test_input.split()


def _get_test_lists():
    for list_type in ["-", "1.", "10.", "- [ ]", "- [x]"]:
        yield list_type + " Hello world", [
            list_type,
            "Hello",
            "world",
        ]


@pytest.mark.parametrize("test_input,expected", _get_test_lists())
def test_lists(test_input: str, expected: List[str]) -> None:
    """Test list within templates."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == expected


def _get_test_lists_in_templates():
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES + STYLE_TEMPLATES:
        for list_type in ["-", "1.", "10.", "- [ ]", "- [x]"]:
            yield template.format(list_type + " Hello" + list_type + " world")


@pytest.mark.parametrize("test_input", _get_test_lists_in_templates())
def test_lists_in_templates(test_input: str) -> None:
    """Test list within templates."""
    tokens = tokenizer.tokenize(test_input)
    assert tokens == [test_input]
