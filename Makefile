.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies in the current Python environment
	pip install --upgrade pip
	python -m pip install .

dev-install:  ## Install dependencies in the current Python environment and install pre-commits
	pip install --upgrade pip
	python -m pip install '.[dev]'
	pre-commit install

freeze:  ## Create frozen, pinned requirements from the current Python environment
	pip list --format=freeze > frozen-requirements.txt

setup-env:  ## Create a new Python virtual environment called 'venv' in ./.venv
	python3 -m venv .venv

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

test: install  ## Run unit tests against installed version of the package
	pytest  -vv tests

test-local:  ## Run unit tests against local files
	python -m pytest  -vv tests

build:  ## Build the package as tar.gz and wheel files
	python -m pip install setuptools wheel build
	python -m build .

test-pypi:  ## Push a build to test PyPI
	python -m pip install twine
	python -m twine upload --repository testpypi dist/*

docs:  ## Create API docs
	sphinx-apidoc -e -o docs/source/ src/plotly_football_pitch
