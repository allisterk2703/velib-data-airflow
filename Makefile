.PHONY: help install-requirements install-requirements-dev clean black isort ruff pre-commit

SRC_DIR := src

help:  ## Show the list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-requirements:  ## Install main dependencies
	@pip install --upgrade pip setuptools wheel
	@pip install -r requirements.txt
	@echo "Main dependencies installed"

install-requirements-dev:  ## Install development dependencies
	@pip install --upgrade pip setuptools wheel
	@pip install -r requirements-dev.txt
	@echo "Development dependencies installed"

clean:  ## Remove temporary files (excluding .venv)
	@rm -rf __pycache__ .pytest_cache *.pyc
	@echo "Temporary files removed"

isort:  ## Sort Python imports
	@echo "Sorting imports with isort..."
	@isort $(SRC_DIR)
	@echo "Imports sorted with isort"

black:  ## Format Python code with Black
	@echo "Formatting code with Black..."
	@black $(SRC_DIR)
	@echo "Code formatted with Black"

ruff:  ## Check and fix Python code with Ruff
	@echo "Checking and fixing code with Ruff..."
	@ruff check $(SRC_DIR) --fix
	@ruff format $(SRC_DIR)
	@echo "Code checked and fixed with Ruff"

pre-commit: isort black # ruff  ## Run all pre-commit checks without Git
	@echo "Pre-commit executed"
