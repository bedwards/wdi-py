#!/bin/bash
set -e

echo "================================"
echo "Running CI checks locally..."
echo "================================"
echo

echo "→ Formatting with ruff..."
ruff format .
echo "✓ Format applied"
echo

echo "→ Linting with ruff..."
ruff check --fix .
echo "✓ Lint passed"
echo

# echo "→ Type checking with dmypy..."
# dmypy run -- wdi --fast-module-lookup
# echo "✓ Type check passed"
# echo

echo "→ Type checking with pyright..."
pyright
echo "✓ pyright passed"
echo

echo "→ Running tests with coverage..."
pytest -q --cov=wdi --cov-report=xml --cov-report=term-missing
echo "✓ Tests passed"
echo

echo "================================"
echo "All checks passed! ✓"
echo "================================"
