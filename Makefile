.PHONY: help install install-dev test coverage lint format typecheck clean examples examples-all db-up db-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make lint          - Check code style"
	@echo "  make format        - Format code"
	@echo "  make typecheck     - Run type checker"
	@echo "  make clean         - Remove generated files"
	@echo "  make examples      - Run example scripts"
	@echo "  make db-up         - Start PostgreSQL database"
	@echo "  make db-down       - Stop PostgreSQL database"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

coverage:
	pytest --cov=wdi --cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy wdi

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

examples:
	@mkdir -p data/output
	@echo "Running examples..."
	@echo ""
	python scripts/examples/inequality_geography.py
	python scripts/examples/development_tradeoffs.py
	python scripts/examples/wealth_wellbeing.py
	python scripts/examples/labor_productivity.py
	python scripts/examples/education_opportunity.py
	python scripts/examples/debt_development.py
	python scripts/examples/healthcare_access.py
	python scripts/examples/gender_gaps.py
	python scripts/examples/wage_stagnation.py
	python scripts/examples/imperial_extraction.py
	python scripts/examples/education_debt.py
	python scripts/examples/military_healthcare.py
	python scripts/examples/automation_unemployment.py
	@echo ""
	@echo "✓ All examples generated in data/output/"

db-up:
	docker compose -f db/server.yml up -d
	@echo "PostgreSQL running on localhost:5432"

db-down:
	docker compose -f db/server.yml down
