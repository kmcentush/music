.PHONY: install
install:
	python -m pip install --upgrade pip
	echo "https://${GITHUB_ACCESS_TOKEN}:@github.com" > ~/.git-credentials
	git config --global credential.helper store
	pip install -e . --upgrade --upgrade-strategy eager
	rm -f ~/.git-credentials

.PHONY: dev_install
dev_install:
	python -m pip install --upgrade pip
	echo "https://${GITHUB_ACCESS_TOKEN}:@github.com" > ~/.git-credentials
	git config --global credential.helper store
	pip install -e .[dev] --upgrade --upgrade-strategy eager
	rm -f ~/.git-credentials
	pre-commit install

.PHONY: format
format:
	ruff format .
	ruff check . --fix
	mypy . --ignore-missing-imports

.PHONY: test_format
test_format:
	ruff format . --check
	ruff check .
	mypy . --ignore-missing-imports

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=src tests/ -s

VERSION := ${shell python src/PLACEHOLDER/__init__.py}

.PHONY: docker
docker:
	docker build . \
		--build-arg GIT_ACCESS_TOKEN=${GITHUB_ACCESS_TOKEN} \
		-t cuberg/PLACEHOLDER:${VERSION}
		-f deployment/Dockerfile .