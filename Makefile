# Makefile for origami-simulator
# Usage: make <target>

PYTHON ?= python
VENV  ?= .venv
PY    ?= $(VENV)/bin/python

.PHONY: help venv install test example render examples lint format clean ci

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

venv: ## Create a virtual environment
	python -m venv $(VENV)

install: venv ## Install the package and dev dependencies in editable mode
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e ".[dev]"

test: ## Run the test suite
	$(PY) -m pytest -q

example: ## Run the minimal example
	$(PY) origami_engine/example.py

render: ## Render the reference pattern to individual_simulation.mp4
	$(PY) origami_engine/render_individual.py

examples: ## Run all example scripts
	@for f in examples/0*.py; do echo "== $$f"; $(PY) "$$f"; done

lint: ## Run ruff lint + format check
	$(PY) -m ruff check .
	$(PY) -m ruff format --check .

format: ## Apply ruff formatting
	$(PY) -m ruff format .
	$(PY) -m ruff check --fix .

typecheck: ## Run mypy on the package
	$(PY) -m mypy origami_engine

clean: ## Remove generated artifacts and caches
	rm -f render_report.json render_report.md individual_simulation.mp4
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
