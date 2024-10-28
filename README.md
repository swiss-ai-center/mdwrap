<div style="text-align: center">
  <h1>MDWrap</h1>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit">
  </a>
  <a href=".github/workflows/lint-and-test.yml">
    <img src="https://github.com/leonardcser/mdwrap/actions/workflows/lint-and-test.yml/badge.svg" alt="lint-and-test">
  </a>
</div>

<h2>Table of Contents</h2>

- [Overview](#overview)
- [Pre-commit Hook](#pre-commit-hook)
- [Installation](#installation)
- [Usage](#usage)
  - [Arguments](#arguments)
- [Limitations](#limitations)
- [Alternatives](#alternatives)
- [Contributing](#contributing)
  - [Development](#development)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Releasing](#releasing)
- [References](#references)

## Overview

`mdwrap` is a Python package that wraps text in Markdown files to a specified
width. It also implements basic newline formatting and trailing whitespace
removal. This package was built for compatibility with
[Material for MKDocs](https://squidfunk.github.io/mkdocs-material/).

The motivation for this project was to have a lightweight package with no
external dependencies that works well with Material for MkDocs for wrapping and
basic formatting of Markdown files.

## Pre-commit Hook

You can use `mdwrap` as a pre-commit hook to automatically wrap your Markdown
files. To do so, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/swiss-ai-center/mdwrap
      rev: 0.2.4
      hooks:
        - id: mdwrap
          args: [--print-width, "80", --fmt]
```

## Installation


```bash
pip install git+https://github.com/swiss-ai-center/mdwrap.git@0.2.4
```

## Usage

```bash
mdwrap [-h] [--print-width PRINT_WIDTH] [--fmt] [--unwrap] [--check]
       [--ignore IGNORE] [--ignore-extend IGNORE_EXTEND] [--version]
       targets [targets ...]
```


```bash
# To format (wrap) a file:
mdwrap file.md
# To format (wrap + remove trailing newline + whitespace) a file:
mdwrap --fmt file.md
# To check (wrap) a file:
mdwrap --check file.md
# To check (wrap + remove trailing newline + whitespace) a file:
mdwrap --fmt --check file.md
```

### Arguments

| Argument                | Description                                              | Default                |
| ----------------------- | -------------------------------------------------------- | ---------------------- |
| `-h`, `--help`          | Show the help message and exit                           |                        |
| `-v`, `--version`       | Show the version and exit                                |                        |
| `--print-width`         | Maximum width of a line                                  | `80`                   |
| `--fmt`                 | Format files                                             | `False`                |
| `--unwrap`              | Unwrap files                                             | `False`                |
| `--check`               | Check if files are formatted                             | `False`                |
| `-i`, `--ignore`        | Ignore files matching this glob pattern                  | check with `mdwrap -h` |
| `-I`, `--ignore-extend` | Extend the default ignore pattern with this glob pattern | `None`                 |
| `targets`               | Files or folders of files to format                      |                        |

## Limitations

One limitation of `mdwrap` is that it does not yet support wrapping quote
blocks.

## Alternatives

- [`mdformat`](https://mdformat.readthedocs.io) is a Python package that formats
  Markdown files. It is more feature-rich than `mdwrap` however it does not
  support Material for MkDocs admonitions entirely.
- [`prettier`](https://prettier.io) is a powerful code formatter that supports
  Markdown. It's only downside is that it needs a node environment to run.

## Contributing

### Development

Create and enable a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
pip install .
```

Install the pre-commit hooks:

```bash
pre-commit install
```

### Testing

To run the tests:

```bash
pytest
```

### Linting

To lint the code:

```bash
pre-commit run -a
```

### Releasing

1. Make sure to first update the versions in this file.
2. Update the [CHANGELOG](/CHANGELOG).
3. Next, release a new version by running the following:

```bash
# Bump the version in pyproject.toml
sed -i 's/version = ".*"/version = "0.x.y"/' pyproject.toml
# Create a new tag
git tag <version> main
# Push the tag
git push origin <version>
```
4. Update the changes in the new
   [GitHub release](https://github.com/csia-pme/mdwrap/releases/latest).
5. Finally, update the version in the pre-commit hook in
   [.pre-commit-config.yaml](/.pre-commit-config.yaml).

## References

This project is built with the following tools:

- [`pre-commit`](https://pre-commit.com/)
- [`pytest`](https://docs.pytest.org/)
- [`flake8`](https://flake8.pycqa.org/en/latest/)
- [`black`](https://black.readthedocs.io/en/stable/)

It is also inspired by the following projects:

- [`black`](https://black.readthedocs.io/en/stable/)
- [`prettier`](https://prettier.io/)
