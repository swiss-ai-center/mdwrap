<div style="text-align: center">
    <h1>MDWrap</h1> <a href="https://www.python.org">
        <img
        src="https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white"
        alt="python">
    </a> <a href="https://github.com/pre-commit/pre-commit">
        <img
        src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"
        alt="pre-commit">
    </a> <a href=".github/workflows/lint-and-test.yml">
        <img
        src="https://github.com/leonardcser/mdwrap/actions/workflows/lint-and-test.yml/badge.svg"
        alt="lint-and-test">
    </a>
</div>

<h2>Table of Contents</h2>

- [Overview](#overview)
- [Pre-commit Hook](#pre-commit-hook)
- [Installation](#installation)
  - [With pip](#with-pip)
  - [With poetry](#with-poetry)
- [Usage](#usage)
  - [Arguments](#arguments)
- [Contributing](#contributing)
  - [Development](#development)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Releasing](#releasing)
- [References](#references)

## Overview

MDWrap is a Python package that wraps text in Markdown files to a specified
width. Its is compatible with
[Material for MKDocs](https://squidfunk.github.io/mkdocs-material/).

## Pre-commit Hook

You can use MDWrap as a pre-commit hook to automatically wrap your Markdown
files. To do so, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/csia-pme/mdwrap
      rev: 0.1.0
      hooks:
        - id: mdwrap
          args: [--print-width, "80", --fmt]
```

## Installation

### With pip

```bash
pip install git+https://github.com/csia-pme/mdwrap.git@0.1.0
```

### With poetry

```bash
poetry add git+https://github.com/csia-pme/mdwrap.git@0.1.0
```

## Usage

```bash
mdwrap [options] <file or directory>
```

### Arguments

| Argument        | Description                                   | Default |
| --------------- | --------------------------------------------- | ------- |
| `-h`, `--help`  | Show the help message and exit                |         |
| `--print-width` | Maximum width of a line                       | `80`    |
| `--fmt`         | Format the file(s) (basic newline formatting) | `false` |
| `--unwrap`      | Unwrap the file(s)                            | `false` |
| `--check`       | Check if the file(s) is/are formatted         | `false` |

## Contributing

### Development

Firstly, install the pre-commit hooks:

```bash
pre-commit install
```

Then, install the development dependencies:

```bash
poetry install
```

### Testing

To run the tests:

```bash
poetry run pytest
```

### Linting

To lint the code:

```bash
poetry run flake8
poetry run black --check .
```

### Releasing

First, make sure to update the version in this file.

Next, to release a new version:

```bash
poetry version <version>
git tag <version> main
git push origin <version>
```

## References

This project is built with the following tools:

- [`pre-commit`](https://pre-commit.com/)
- [`poetry`](https://python-poetry.org/)
- [`pytest`](https://docs.pytest.org/)
- [`flake8`](https://flake8.pycqa.org/en/latest/)
- [`black`](https://black.readthedocs.io/en/stable/)

It is also inspired by the following projects:

- [`black`](https://black.readthedocs.io/en/stable/)
- [`prettier`](https://prettier.io/)
