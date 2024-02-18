.PHONY: install
install:
	python -m pip install --upgrade pip
	pip install uv
	uv pip install --upgrade uv
	uv pip install --upgrade -e .

.PHONY: dev_install
dev_install:
	python -m pip install --upgrade pip
	pip install uv
	uv pip install --upgrade uv
	uv pip install --upgrade -e .[dev]
	pre-commit install

.PHONY: format
format:
	ruff format .
	ruff check . --fix
	mypy . --install-types --ignore-missing-imports

.PHONY: test_format
test_format:
	ruff format . --check
	ruff check .
	mypy . --install-types --ignore-missing-imports

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=src tests/ -s
