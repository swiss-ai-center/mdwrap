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
- [Installation](#installation)
- [Usage](#usage)
  - [Arguments](#arguments)
- [Contributing](#contributing)
  - [Development](#development)
  - [Testing](#testing)
  - [Linting](#linting)
- [References](#references)

## Overview

MDWrap is a Python package that wraps text in Markdown files to a specified
width. Its is compatible with
[Material for MKDocs](https://squidfunk.github.io/mkdocs-material/).

## Installation

```bash
pip install git+https://https://github.com/leonardcser/mdwrap.git
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
