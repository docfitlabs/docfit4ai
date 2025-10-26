# DocFitLabs for AI - Makefile
# ========================

.PHONY: help install install-dev test test-coverage lint format clean build run ui docker-build docker-run all

# Default target
help:
	@echo "DocFitLabs for AI - Available Commands:"
	@echo ""
	@echo "  install      Install the package"
	@echo "  install-dev  Install with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-coverage Run tests with coverage"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  run          Run the Streamlit UI"
	@echo "  ui           Alias for run"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"
	@echo "  all          Run all checks and build"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 src/
	mypy src/

format:
	black src/
	isort src/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python setup.py sdist bdist_wheel

# Run applications
run:
	streamlit run src/ui/streamlit_app.py

ui: run

# Docker
docker-build:
	docker build -t docfit4ai .

docker-run:
	docker run -p 8501:8501 docfit4ai

# CLI tools (for testing)
test-ready4ai:
	python src/cli/ready4ai.py --help

test-ready4ai-enhanced:
	python src/cli/ready4ai_enhanced.py --help

test-security4ai:
	python src/cli/security4ai.py --help

test-security4ai-enhanced:
	python src/cli/security4ai_enhanced.py --help

test-obfuscate4ai:
	python src/cli/obfuscate4ai.py --help

test-obfuscate4ai-enhanced:
	python src/cli/obfuscate4ai_enhanced.py --help

# Test all CLI tools
test-cli: test-ready4ai test-ready4ai-enhanced test-security4ai test-security4ai-enhanced test-obfuscate4ai test-obfuscate4ai-enhanced

# All checks
all: clean install-dev lint test build

# Development workflow
dev-setup: install-dev
	@echo "Development environment ready!"
	@echo "Run 'make ui' to start the Streamlit interface"
	@echo "Run 'make test' to run tests"

# Quick start
quick-start: install
	@echo "DocFitLabs for AI installed!"
	@echo "Run 'make ui' to start the web interface"
	@echo "Or use CLI tools: ready4ai, security4ai, obfuscate4ai"
