# Contributing to wdi-py

Thank you for considering contributing to wdi-py! This document provides guidelines for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/bedwards/wdi-py.git
cd wdi-py
```

2. Install development dependencies:
```bash
make install-dev
# or
pip install -e ".[dev]"
```

3. Start the database (if needed):
```bash
make db-up
```

## Code Quality Standards

Before submitting a pull request, ensure your code meets these standards:

### Run Tests
```bash
make test
```

All tests must pass. Aim for high test coverage:
```bash
make coverage
```

### Code Formatting
```bash
make format
```

We use `ruff` for code formatting. The project follows PEP 8 with a 100-character line length.

### Linting
```bash
make lint
```

Code must pass all linting checks.

### Type Checking
```bash
make typecheck
```

All code should include type hints and pass `mypy` checks.

## Project Structure

- `wdi/` - Main package code
  - `sql.py` - Database queries
  - `df.py` - DataFrame operations
  - `chart.py` - Visualization utilities
- `tests/` - Unit tests (mirror the structure of `wdi/`)
- `scripts/examples/` - Example scripts demonstrating package features

## Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_<module>.py`
- Use descriptive test function names: `test_<function>_<scenario>()`
- Aim for >80% code coverage
- Use fixtures for common test data
- Mock external dependencies (database connections, etc.)

Example test structure:
```python
def test_function_basic_case():
    """Test function with basic inputs."""
    result = function(input)
    assert result == expected

def test_function_edge_case():
    """Test function with edge case."""
    with pytest.raises(ValueError):
        function(invalid_input)
```

## Writing Examples

Examples should:
- Be self-contained and runnable
- Focus on one concept or analysis
- Produce exactly two interactive charts (left controls right)
- Include descriptive comments and questions to explore
- Output to `data/output/`

## Pull Request Process

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure all checks pass:
```bash
make format lint typecheck test
```

3. Commit with descriptive messages:
```bash
git commit -m "Add feature: description of what you added"
```

4. Push and create a pull request:
```bash
git push origin feature/your-feature-name
```

5. In your PR description:
   - Describe the changes
   - Link any related issues
   - Include screenshots for visualization changes
   - Note any breaking changes

## Code Style Guidelines

- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use descriptive variable names
- Prefer Polars operations over pandas
- Use Altair's declarative API for visualizations

## Adding New Indicators

When adding support for new WDI indicators:
1. Document the indicator code and name
2. Add helper functions if the indicator requires special handling
3. Create an example script demonstrating its use
4. Update README.md with the new example

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about contributing
- Discussion of design decisions

Thank you for contributing!
