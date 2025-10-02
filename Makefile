.PHONY: help install install-dev test lint format check-quality security clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in production mode
	pip install -e .

install-dev: ## Install package in development mode with all dev dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run tests with coverage
	pytest -v --cov=. --cov-report=html --cov-report=xml

test-fast: ## Run tests without coverage
	pytest -v

lint: ## Run all linters
	flake8 .
	pylint *.py
	mypy . --ignore-missing-imports

format: ## Format code with black and isort
	black .
	isort .

format-check: ## Check if code is properly formatted
	black --check .
	isort --check-only .

check-quality: ## Run quality checks (complexity, maintainability)
	radon cc . --min B --show-complexity
	xenon . --max-absolute B --max-modules A --max-average A

security: ## Run security checks
	bandit -r . -f json -o bandit-report.json
	safety check --json --output safety-report.json

quality-gate: format-check lint check-quality security test ## Run complete quality gate

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

ci: ## Run CI pipeline locally
	$(MAKE) quality-gate

all: clean install-dev quality-gate ## Clean, install, and run all quality checks
