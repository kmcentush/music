# Python Package Template
Last updated: 2025-07-19

## Installation
1. Install [uv](https://github.com/astral-sh/uv) for your system.
2. Install [make](https://www.gnu.org/software/make/) for your system.
3. Clone this repository and `cd` into it.
4. Run `uv venv --python 3.13` to initialize a virtual environment with Python 3.13.
5. Activate your new virtual environment.
   - If you're using an IDE, select the virtual environment as your
default Python interpreter, then restart the terminal.
6. Run `make install` to install all requirements, or `make dev_install` to also include optional dependencies
required for code formatting, tests, etc.

## Updating Dependencies
1. Edit the `pyproject.toml` manually.
2. Run `make compile`, followed by `make install` or `make dev_install`.

Alternatively, you can use `uv add`/`uv remove` to update dependencies, compile the lock file, and install with a single command.

## Formatting and Tests
1. Follow the `Installation` section above, being sure to use `make dev_install` instead of `make install`.
2. Run `make format` to lint and format all code using `ruff`, then check types using `ty`.
3. Run `make test` to run tests and output a code coverage report.

## Version Bumping
- Edit `__version__` in `src/music/__init__.py`
