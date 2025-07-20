.PHONY: install
install:
	uv sync --no-group dev
	uv pip install -e . --no-deps

.PHONY: dev_install
dev_install:
	uv sync
	uv pip install -e . --no-deps
	pre-commit install

.PHONY: compile
compile:
	uv lock

.PHONY: format
format:
	ruff check . --fix
	ruff format .
	ty check .

.PHONY: test
test:
	pytest --cov-report term-missing --cov=src tests/ -s
