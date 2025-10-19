# wdi-py

[![Tests](https://github.com/bedwards/wdi-py/actions/workflows/test.yml/badge.svg)](https://github.com/bedwards/wdi-py/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/bedwards/wdi-py/branch/main/graph/badge.svg)](https://codecov.io/gh/bedwards/wdi-py)
[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python toolkit for analyzing World Bank Development Indicators (WDI) data with interactive visualizations. Query a PostgreSQL database of WDI data, manipulate it with Polars, and create linked interactive charts with Altair.

## Features

- **SQL Module** (`wdi.sql`): Type-safe queries against PostgreSQL WDI database
- **DataFrame Module** (`wdi.df`): Polars-based data manipulation and analysis
- **Chart Module** (`wdi.chart`): Interactive Altair visualizations with linked filtering
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

# Get GDP per capita and life expectancy for 2021
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita
    indicator_y="SP.DYN.LE00.IN",   # Life expectancy
    year=2021,
    include_region=True
)

# Create interactive scatter plot with selection brush
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="x_value",
    y="y_value",
    color="region",
    title="GDP per Capita vs Life Expectancy (2021)",
    x_title="GDP per Capita (US$, log scale)",
    y_title="Life Expectancy (years)",
    log_x=True
)

# Create bar chart that updates based on scatter selection
bar = wdi.chart.bar_chart_filtered(
    df,
    x="region",
    y="count()",
    color="region",
    title="Countries by Region (Selected)",
    selection=brush
)

# Save linked charts side-by-side
wdi.chart.save_linked_charts(
    scatter, 
    bar, 
    "wealth_wellbeing.html",
    overall_title="Beyond GDP: Exploring the wealth-health relationship"
)
```

## Data

This project uses World Bank Development Indicators (WDI) data.

**Download:** [WDI_CSV.zip](https://databank.worldbank.org/data/download/WDI_CSV.zip)

Extract the downloaded file to `data/input/WDI_CSV/` in your project directory before importing.

## Database Setup

The package requires a PostgreSQL database with WDI data.

```bash
# 1. Download and extract WDI data to data/input/WDI_CSV/

# 2. Start PostgreSQL
make db-up
# or
docker compose -f db/server.yml up -d

# 3. Import WDI data
./scripts/db-import.sh

# 4. Verify the import
./scripts/db.sh scripts/queries/record_counts.sql
```

The import script creates three tables in the `wdi` schema:
- `wdi.countries` - Country metadata (region, income group)
- `wdi.indicators` - Indicator definitions and metadata
- `wdi.values` - Indicator values by country and year

## Module Documentation

### SQL Module (`wdi.sql`)

Query the WDI PostgreSQL database with type-safe functions.

```python
import wdi

# Get all countries in a region
countries = wdi.sql.get_countries(region="Sub-Saharan Africa")

# Search for indicators by keyword
indicators = wdi.sql.get_indicators(search="GDP")

# Get indicator values with flexible filtering
values = wdi.sql.get_values(
    indicator_code="NY.GDP.MKTP.CD",
    year=2020
)

# Get time range
values = wdi.sql.get_values(
    indicator_code="SP.DYN.LE00.IN",
    start_year=2010,
    end_year=2020
)

# Filter by country
values = wdi.sql.get_values(
    indicator_code="NY.GDP.PCAP.CD",
    country_code="USA"
)
```

**Key functions:**
- `get_connection()` - Create database connection
- `query(sql, conn)` - Execute raw SQL, return Polars DataFrame
- `get_countries(region, income_group)` - Query countries table
- `get_indicators(topic, search)` - Query indicators table
- `get_values(indicator_code, year, country_code, start_year, end_year)` - Query values table

### DataFrame Module (`wdi.df`)

Analyze data with Polars-based utilities.

```python
import wdi

# Get indicator data with country metadata
df = wdi.df.get_indicator_data(
    "NY.GDP.PCAP.CD",
    year=2020,
    include_region=True,
    include_income_group=True
)

# Get paired indicators for scatter plots
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita
    indicator_y="SP.DYN.LE00.IN",   # Life expectancy
    year=2020,
    include_region=True
)

# Get time series for multiple countries
df = wdi.df.get_time_series(
    indicator_code="NY.GDP.MKTP.CD",
    country_codes=["USA", "CHN", "DEU"],
    start_year=2000,
    end_year=2020
)

# Calculate growth rates
df_growth = wdi.df.calculate_growth_rate(df, periods=1)

# Rank countries by value
df_ranked = wdi.df.rank_countries(df, value_col="value", descending=True)

# Aggregate by region
df_regional = wdi.df.aggregate_by_region(df, agg_func="mean")

# Filter to latest year per country
df_latest = wdi.df.filter_latest_year(df)

# Pivot to wide format (years as columns)
df_wide = wdi.df.pivot_wide(df)
```

**Key functions:**
- `get_indicator_data()` - Single indicator with optional metadata
- `get_indicator_pairs()` - Two indicators for scatter plots
- `get_time_series()` - Time series for multiple countries
- `pivot_wide()` - Transform to wide format
- `calculate_growth_rate()` - Period-over-period growth
- `rank_countries()` - Rank by value
- `aggregate_by_region()` - Regional aggregation
- `filter_latest_year()` - Most recent data per country

### Chart Module (`wdi.chart`)

Create interactive Altair visualizations with linked filtering.

```python
import wdi

# Scatter plot with interval selection
scatter, brush = wdi.chart.scatter_with_filter(
    df,
    x="x_value",
    y="y_value",
    color="region",
    tooltip=["country_name", "x_value", "y_value"],
    title="GDP vs Life Expectancy",
    log_x=True,
    log_y=False,
    width=500,
    height=500
)

# Bar chart filtered by selection
bar = wdi.chart.bar_chart_filtered(
    df,
    x="income_group",
    y="count()",
    color="income_group",
    title="Income Distribution",
    selection=brush,
    width=450,
    height=500
)

# Histogram filtered by selection
histogram = wdi.chart.histogram_filtered(
    df,
    column="value",
    bins=30,
    title="Value Distribution",
    selection=brush
)

# Line chart for time series
line = wdi.chart.line_chart_filtered(
    df,
    x="year",
    y="value",
    color="country_code",
    title="Trend Over Time",
    selection=brush
)

# Save two charts side-by-side
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename="analysis.html",
    overall_title="Economic Development Analysis"
)
```

**Key functions:**
- `scatter_with_filter()` - Scatter plot with interval selection brush
- `bar_chart_filtered()` - Bar chart that responds to selection
- `histogram_filtered()` - Histogram that responds to selection
- `line_chart_filtered()` - Line chart that responds to selection
- `save_linked_charts()` - Save two charts side-by-side to HTML

## Examples

Interactive examples are in `scripts/examples/`. Each produces an HTML file with two linked charts where selecting data in the left chart filters the right chart.

```bash
# Run a single example
python scripts/examples/inequality_geography.py

# Run all examples at once
make examples

# View output
open data/output/inequality_geography.html
```

### Available Examples

- **`inequality_geography.py`** - Income inequality (Gini coefficient) across regions. Select countries to see regional distribution.

- **`development_tradeoffs.py`** - Economic growth vs carbon emissions. Select countries to see emission distribution.

- **`wealth_wellbeing.py`** - GDP per capita vs life expectancy. Select countries to see income group distribution.

- **`labor_productivity.py`** - Employment rates vs economic output. Select countries to see regional patterns.

- **`education_opportunity.py`** - Educational attainment vs unemployment. Select countries to see income distribution.

- **`debt_development.py`** - External debt burdens vs GDP growth. Select countries to see regional debt patterns.

- **`healthcare_access.py`** - Health expenditure vs infant mortality. Select countries to see spending trends over time.

- **`gender_gaps.py`** - Gender gaps in labor force participation. Select countries to see gap distribution.

Each example demonstrates:
- Querying specific WDI indicators
- Creating paired indicator datasets
- Building interactive scatter plots with selection
- Creating filtered secondary visualizations
- Saving linked charts to HTML

## Development

### Quick Commands

```bash
# Run all tests
make test

# Run tests with coverage report
make coverage

# Lint code
make lint

# Format code
make format

# Type check
make typecheck

# Run all examples
make examples

# Clean generated files
make clean

# Start/stop database
make db-up
make db-down
```

### Manual Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=wdi --cov-report=html

# Lint and format
ruff check .
ruff format .

# Type check
mypy wdi
pyright
```

### Running CI Checks Locally

```bash
./scripts/ci.sh
```

This runs the same checks as GitHub Actions: formatting, linting, type checking, and tests with coverage.

## Project Structure

```
wdi-py/
├── wdi/                    # Main package
│   ├── __init__.py        # Package initialization
│   ├── sql.py             # PostgreSQL query utilities
│   ├── df.py              # Polars data manipulation
│   └── chart.py           # Altair visualization utilities
├── tests/                 # Unit tests (mirrors wdi/ structure)
│   ├── test_sql.py
│   ├── test_df.py
│   └── test_chart.py
├── scripts/
│   ├── examples/          # Interactive visualization examples
│   ├── queries/           # SQL query examples
│   ├── ddl/              # Database schema and import
│   ├── db.sh             # Database client helper
│   ├── db-import.sh      # Import WDI data
│   ├── db-server.sh      # Start database
│   └── ci.sh             # Run CI checks locally
├── db/                    # Docker Compose configs
│   ├── server.yml        # PostgreSQL server
│   └── client.yml        # PostgreSQL client
├── data/
│   ├── input/            # WDI CSV files (gitignored)
│   └── output/           # Generated visualizations (gitignored)
├── pyproject.toml        # Project configuration
├── Makefile              # Common development tasks
├── README.md             # This file
├── LICENSE               # MIT License
└── CONTRIBUTING.md       # Contribution guidelines
```

## Database Schema

The `wdi` schema contains three tables:

### `wdi.countries`
- `country_code` (VARCHAR(3), primary key) - ISO 3-letter code
- `country_name` (TEXT) - Official country name
- `region` (TEXT) - World Bank region classification
- `income_group` (TEXT) - Income level classification

### `wdi.indicators`
- `indicator_code` (VARCHAR(50), primary key) - WDI indicator code
- `indicator_name` (TEXT) - Human-readable name
- `topic` (TEXT) - Topic category
- `short_definition` (TEXT) - Brief description
- `long_definition` (TEXT) - Full description
- Plus additional metadata fields

### `wdi.values`
- `id` (BIGSERIAL, primary key)
- `country_code` (VARCHAR(3), foreign key)
- `indicator_code` (VARCHAR(50), foreign key)
- `year` (INTEGER) - Year of observation
- `value` (NUMERIC) - Indicator value
- Plus denormalized country_name and indicator_name for convenience

Indexes support efficient filtering by country, indicator, and year.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Before submitting a pull request:

```bash
# Ensure all checks pass
make format
make lint
make typecheck
make test
```

Or use the CI script:

```bash
./scripts/ci.sh
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Data source: [World Bank Development Indicators](https://databank.worldbank.org/)

The World Development Indicators (WDI) is the World Bank's premier compilation of cross-country comparable data on development.
