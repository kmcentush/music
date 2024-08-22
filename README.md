# music

Pull Spotify data using their API and explore how track features can be used to classify music into playlists.

## Installation
1. Install [uv](https://github.com/astral-sh/uv) for your system.
2. Install [make](https://www.gnu.org/software/make/) for your system.
3. Clone this repository and `cd` into it.
4. Run `uv venv --python 3.12` to initialize a virtual environment with Python 3.12.
5. Run `make install` to install all requirements, or `make dev_install` to install all requirements plus additional
dependencies required for code formatting, tests, etc.

## Version Bumping
- Edit `__version__` in `src/music/__init__.py`
