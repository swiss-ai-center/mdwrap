from mdwrap.classes.md_tokenizer import MDTokenizer

tokenizer = MDTokenizer()

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

PUNCTUATION = [".", ",", "!", "?", ":", ";", "-", "(", ")", "[", "]", "{", "}"]


def test_image_and_link():
    """Test images and links."""
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        text = "Hello world"
        expected = template.format(text)
        tokens = tokenizer.tokenize(expected)
        assert tokens == [expected]


def test_image_and_link_punctuation():
    """Test punctuation included in images and links."""
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for punctuation in PUNCTUATION:
            expected = "Hello " + punctuation + template.format("world") + punctuation
            tokens = tokenizer.tokenize(expected)
            assert tokens == [
                "Hello",
                punctuation + template.format("world") + punctuation,
            ]


def test_image_and_link_multiple():
    """Test multiple images and links in the same string."""
    for template1 in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for template2 in IMAGE_TEMPLATES + LINK_TEMPLATES:
            expected = template1.format("Hello") + " " + template2.format("world")
            tokens = tokenizer.tokenize(expected)
            assert tokens == [template1.format("Hello"), template2.format("world")]


def test_style():
    """Test bold and italic."""
    for template in STYLE_TEMPLATES:
        text = "Hello world"
        expected = template.format(text)
        tokens = tokenizer.tokenize(expected)
        assert tokens == [expected]


def test_style_punctuation():
    """Test punctuation included in bold and italic."""
    for template in STYLE_TEMPLATES:
        for punctuation in PUNCTUATION:
            expected = "Hello " + punctuation + template.format("world") + punctuation
            tokens = tokenizer.tokenize(expected)
            assert tokens == [
                "Hello",
                punctuation + template.format("world") + punctuation,
            ]


def test_style_muliple():
    """Test multiple bold and italic in the same string."""
    for template1 in STYLE_TEMPLATES:
        for template2 in STYLE_TEMPLATES:
            expected = template1.format("Hello") + " " + template2.format("world")
            tokens = tokenizer.tokenize(expected)
            assert tokens == [template1.format("Hello"), template2.format("world")]


def test_style_within_image_or_link():
    """Test style within images and links."""
    for template in IMAGE_TEMPLATES + LINK_TEMPLATES:
        for style_template in STYLE_TEMPLATES:
            expected = template.format(style_template.format("Hello"))
            tokens = tokenizer.tokenize(expected)
            assert tokens == [expected]


def test_mix():
    """Test mixing all templates."""
    for template1 in TEMPLATES:
        for template2 in TEMPLATES:
            expected = template1.format("Hello") + " " + template2.format("world")
            tokens = tokenizer.tokenize(expected)
            assert tokens == [template1.format("Hello"), template2.format("world")]
