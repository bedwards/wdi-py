# wdi-py

[![Tests](https://github.com/bedwards/wdi-py/actions/workflows/test.yml/badge.svg)](https://github.com/bedwards/wdi-py/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/bedwards/wdi-py/branch/main/graph/badge.svg)](https://codecov.io/gh/bedwards/wdi-py)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python toolkit for analyzing World Bank Development Indicators (WDI) data with interactive visualizations.

## Features

- **SQL Module**: Simple, type-safe queries against PostgreSQL WDI database
- **DataFrame Module**: Polars-based data manipulation and analysis
- **Chart Module**: Interactive Altair visualizations with linked filtering
- **Interactive Examples**: Two-chart layouts where selections in one chart filter the other

## Installation

```bash
# Install package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
import wdi

# Get GDP data for 2020 with regional information
df = wdi.df.get_indicator_data(
    "NY.GDP.MKTP.CD",
    year=2020,
    include_region=True
)

# Create interactive scatter plot with bar chart
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="value",
    y="country_name",
    color="region",
    title="GDP by Country (2020)"
)

bar = wdi.chart.bar_chart_filtered(
    df,
    x="region",
    y="count()",
    title="Countries by Region",
    selection=brush
)

# Save linked charts
wdi.chart.save_linked_charts(scatter, bar, "gdp_analysis.html")
```

## Modules

### SQL (`wdi.sql`)

Query the WDI PostgreSQL database:

```python
# Get all countries in a region
countries = wdi.sql.get_countries(region="Sub-Saharan Africa")

# Search for indicators
indicators = wdi.sql.get_indicators(search="GDP")

# Get indicator values
values = wdi.sql.get_values(
    indicator_code="NY.GDP.MKTP.CD",
    start_year=2010,
    end_year=2020
)
```

### DataFrame (`wdi.df`)

Analyze data with Polars:

```python
# Get paired indicators for scatter plots
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita
    indicator_y="SP.DYN.LE00.IN",   # Life expectancy
    year=2020,
    include_region=True
)

# Calculate growth rates
df_growth = wdi.df.calculate_growth_rate(df, periods=1)

# Rank countries
df_ranked = wdi.df.rank_countries(df, value_col="value")

# Aggregate by region
df_regional = wdi.df.aggregate_by_region(df, agg_func="mean")
```

### Chart (`wdi.chart`)

Create interactive visualizations:

```python
# Scatter plot with selection
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="x_value",
    y="y_value",
    color="region",
    log_x=True,
    title="GDP vs Life Expectancy"
)

# Filtered bar chart
bar = wdi.chart.bar_chart_filtered(
    df,
    x="income_group",
    y="count()",
    selection=brush,
    title="Income Distribution"
)

# Save both charts side-by-side
wdi.chart.save_linked_charts(
    scatter,
    bar,
    "analysis.html",
    overall_title="Economic Development Analysis"
)
```

## Examples

Interactive examples are in `scripts/examples/`. Each produces an HTML file with two linked charts:

```bash
# Run an example
python scripts/examples/inequality_geography.py

# View output
open data/output/inequality_geography.html
```

Available examples:
- `inequality_geography.py` - Income inequality (Gini coefficient) across regions
- `development_tradeoffs.py` - Economic growth vs carbon emissions
- `wealth_wellbeing.py` - GDP per capita vs life expectancy
- `labor_productivity.py` - Employment rates vs economic output
- `education_opportunity.py` - Educational attainment vs unemployment
- `debt_development.py` - External debt burdens vs GDP growth
- `healthcare_access.py` - Health expenditure vs infant mortality

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=wdi --cov-report=html

# Lint code
ruff check .
ruff format .

# Type check
mypy wdi
```

## Database Setup

The package expects a PostgreSQL database with WDI data. See the `scripts/ddl/import.sql` file for the schema.

```bash
# Start PostgreSQL
docker compose -f db/server.yml up -d

# Import WDI data (download from World Bank first)
./scripts/db.sh scripts/ddl/import.sql
```

## Project Structure

```
wdi-py/
├── wdi/                    # Main package
│   ├── __init__.py
│   ├── sql.py             # PostgreSQL queries
│   ├── df.py              # Polars data manipulation
│   └── chart.py           # Altair visualizations
├── tests/                 # Unit tests
│   ├── test_sql.py
│   ├── test_df.py
│   └── test_chart.py
├── scripts/
│   ├── examples/          # Interactive visualization examples
│   ├── queries/           # SQL query examples
│   └── ddl/              # Database schema
├── db/                    # Docker compose configs
├── pyproject.toml        # Project configuration
└── README.md
```

## Contributing

Contributions are welcome! Please ensure:
- Tests pass: `pytest`
- Code is formatted: `ruff format .`
- Type hints are correct: `mypy wdi`
- Coverage remains high: `pytest --cov=wdi`

## License

MIT# wdi-py

[![Tests](https://github.com/bedwards/wdi-py/actions/workflows/test.yml/badge.svg)](https://github.com/bedwards/wdi-py/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/bedwards/wdi-py/branch/main/graph/badge.svg)](https://codecov.io/gh/bedwards/wdi-py)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python toolkit for analyzing World Bank Development Indicators (WDI) data with interactive visualizations.

## Features

- **SQL Module**: Simple, type-safe queries against PostgreSQL WDI database
- **DataFrame Module**: Polars-based data manipulation and analysis
- **Chart Module**: Interactive Altair visualizations with linked filtering
- **Interactive Examples**: Two-chart layouts where selections in one chart filter the other

## Installation

```bash
# Install package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
import wdi

# Get GDP data for 2020 with regional information
df = wdi.df.get_indicator_data(
    "NY.GDP.MKTP.CD",
    year=2020,
    include_region=True
)

# Create interactive scatter plot with bar chart
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="value",
    y="country_name",
    color="region",
    title="GDP by Country (2020)"
)

bar = wdi.chart.bar_chart_filtered(
    df,
    x="region",
    y="count()",
    title="Countries by Region",
    selection=brush
)

# Save linked charts
wdi.chart.save_linked_charts(scatter, bar, "gdp_analysis.html")
```

## Modules

### SQL (`wdi.sql`)

Query the WDI PostgreSQL database:

```python
# Get all countries in a region
countries = wdi.sql.get_countries(region="Sub-Saharan Africa")

# Search for indicators
indicators = wdi.sql.get_indicators(search="GDP")

# Get indicator values
values = wdi.sql.get_values(
    indicator_code="NY.GDP.MKTP.CD",
    start_year=2010,
    end_year=2020
)
```

### DataFrame (`wdi.df`)

Analyze data with Polars:

```python
# Get paired indicators for scatter plots
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita
    indicator_y="SP.DYN.LE00.IN",   # Life expectancy
    year=2020,
    include_region=True
)

# Calculate growth rates
df_growth = wdi.df.calculate_growth_rate(df, periods=1)

# Rank countries
df_ranked = wdi.df.rank_countries(df, value_col="value")

# Aggregate by region
df_regional = wdi.df.aggregate_by_region(df, agg_func="mean")
```

### Chart (`wdi.chart`)

Create interactive visualizations:

```python
# Scatter plot with selection
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="x_value",
    y="y_value",
    color="region",
    log_x=True,
    title="GDP vs Life Expectancy"
)

# Filtered bar chart
bar = wdi.chart.bar_chart_filtered(
    df,
    x="income_group",
    y="count()",
    selection=brush,
    title="Income Distribution"
)

# Save both charts side-by-side
wdi.chart.save_linked_charts(
    scatter,
    bar,
    "analysis.html",
    overall_title="Economic Development Analysis"
)
```

## Examples

Interactive examples are in `scripts/examples/`. Each produces an HTML file with two linked charts:

```bash
# Run an example
python scripts/examples/inequality_geography.py

# View output
open data/output/inequality_geography.html
```

Available examples:
- `inequality_geography.py` - Income inequality across regions
- `development_tradeoffs.py` - Economic growth vs environmental impact
- `wealth_wellbeing.py` - GDP per capita vs life expectancy
- `labor_productivity.py` - Working hours vs economic output

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=wdi --cov-report=html

# Lint code
ruff check .
ruff format .

# Type check
mypy wdi
```

## Database Setup

The package expects a PostgreSQL database with WDI data. See the `scripts/ddl/import.sql` file for the schema.

```bash
# Start PostgreSQL
docker compose -f db/server.yml up -d

# Import WDI data
./scripts/db.sh scripts/ddl/import.sql
```

## License

MIT
