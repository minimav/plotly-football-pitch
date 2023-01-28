.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies in the current Python environment and install pre-commits
	pip install --upgrade pip
	pip install -r frozen-requirements.txt
	pre-commit install

freeze:  ## Create frozen, pinned requirements from the current Python environment
	pip list --format=freeze > frozen-requirements.txt

setup-env:  ## Create a new Python virtual environment called 'venv' in ./.venv
	python3 -m venv .venv

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files
