This is a sample markdown file showcasing the usage of admonitions with
different content inside in MkDocs. The lines in the admonitions are
intentionally longer than 80 characters to test the wrapping behavior.

=== "Information"

    This is an information admonition. It provides additional information or
    explanatory content. The lines in this admonition are intentionally longer than
    80 characters to test the wrapping behavior.

    - This is a list item.
    - Another list item.

    You can also include links like
    [Some Informative Link](https://some-informative-link.com/information) within an
    admonition.

    ```python
    def greet(name):
        print(f"Hello, {name}!")
    ```

    === "Nested Information"

        This is a nested information admonition. It can be used to provide further
        details or subcategories within the main admonition. The lines in this nested
        admonition are also longer than 80 characters.

=== "Note"

    This is a note admonition. It is typically used to highlight important points or
    provide additional context. The lines in this admonition are intentionally
    longer than 80 characters to test the wrapping behavior.

    1. This is a numbered list item.
    2. Another numbered list item.

    Here's an example of inline code `print("Hello, World!")`.

    You can also include images like ![MkDocs Logo](mkdocs-logo.png) within a note
    admonition.

=== "Warning"

    This is a warning admonition. It is used to indicate potential issues or things
    to be cautious about. The lines in this admonition are intentionally longer than
    80 characters to test the wrapping behavior.

    - This is a bulleted list item.
    - Another bulleted list item.

    You can refer to external references like [This][1] within a warning admonition.

    [1]: https://some-external-reference.com/warning
