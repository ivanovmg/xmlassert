# Copyright (c) 2025 Maxim Ivanov
# SPDX-License-Identifier: MIT

.PHONY: help tests lint format typecheck build publish clean install-dev

# Default target
help:
	@echo "Available commands:"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make tests        - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code"
	@echo "  make typecheck    - Run type checking"
	@echo "  make check        - Run all checks (lint, format, typecheck, tests)"
	@echo "  make build        - Build package"
	@echo "  make publish      - Build and publish to PyPI"
	@echo "  make clean        - Clean build artifacts"

# Install development dependencies
install-dev:
	pip install -e ".[dev]"

# Run tests with coverage
tests:
	python -m pytest --cov=src/xmlassert --cov-report=term-missing --cov-report=html -v

# Run linting checks
lint:
	ruff check src/xmlassert tests

# Format code
format:
	ruff check --select I --fix  # fix imports
	ruff format src/xmlassert tests

# Check formatting without making changes
format-check:
	ruff format --check src/xmlassert tests

# Run type checking
typecheck:
	mypy src/xmlassert tests

# Run all checks: lint, format check, typecheck, and tests
check: lint format-check typecheck tests

# Build package
build:
	python -m build

# Build and publish to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD)
publish: build
	python -m twine upload dist/*

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml

# Install package in development mode
develop:
	pip install -e .

# Run tests in watch mode (requires pytest-watch)
watch:
	ptw --onpass "echo ? Tests passed" --onfail "echo ? Tests failed"

# Generate coverage report
coverage:
	python -m pytest --cov=src/xmlassert --cov-report=html
	@echo "Coverage report generated at htmlcov/index.html"

# Check for security vulnerabilities
safety:
	pip install safety
	safety check

# Update dependencies
update-deps:
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"

# Show dependency tree
deps-tree:
	pip install pipdeptree
	pipdeptree

# Run benchmarks (if you add benchmarks later)
benchmark:
	@echo "Benchmarks not yet implemented"

# Helpers for CI
ci-install:
	pip install -e ".[dev]"

ci-test:
	python -m pytest --cov=src/xmlassert --cov-report=xml

ci-lint:
	ruff check src/xmlassert tests

ci-format:
	ruff format --check src/xmlassert tests

ci-typecheck:
	mypy src/xmlassert tests
