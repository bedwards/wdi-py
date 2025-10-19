# Examples Section for README.md

Replace the existing "Available Examples" section in README.md with this:

---

## Available Examples

Interactive examples are in `scripts/examples/`. Each produces an HTML file with two linked charts where selecting data in the left chart filters the right chart.

```bash
# Run original examples
make examples

# Run ALL examples (original + new critical political economy examples)
make examples-all

# Run a single example
python scripts/examples/inequality_geography.py

# View output
open data/output/inequality_geography.html
```

### Original Examples

- **`inequality_geography.py`** - Income inequality (Gini coefficient) across regions. Select countries to see regional distribution.

- **`development_tradeoffs.py`** - Economic growth vs carbon emissions. Select countries to see emission distribution.

- **`wealth_wellbeing.py`** - GDP per capita vs life expectancy. Select countries to see income group distribution.

- **`labor_productivity.py`** - Employment rates vs economic output. Select countries to see regional patterns.

- **`education_opportunity.py`** - Educational attainment vs unemployment. Select countries to see income distribution.

- **`debt_development.py`** - External debt burdens vs GDP growth. Select countries to see regional debt patterns.

- **`healthcare_access.py`** - Health expenditure vs infant mortality. Select countries to see spending trends over time.

- **`gender_gaps.py`** - Gender gaps in labor force participation. Select countries to see gap distribution.

### New: Critical Political Economy Examples

Inspired by Jason Hickel and David Graeber's critical analysis of capitalism, inequality, and power structures. These examples are US-centric but compare to other nations to reveal structural differences.

**Pattern**: Bar chart on left allows selection, which filters time series on right.

#### `wage_stagnation.py` - The Productivity-Pay Gap
- **Left**: GDP per worker across wealthy nations (bar chart)
- **Right**: Productivity trends over time (line chart, 1990-2023)
- **Question**: Where has productivity growth gone if not to workers?
- **Insight**: Examines whether worker compensation has kept pace with productivity in the US vs. social democracies.

#### `imperial_extraction.py` - Following the Capital Flows
- **Left**: Foreign Direct Investment net inflows by country (bar chart)
- **Right**: FDI flows over time (line chart, 1990-2023)
- **Question**: Who invests where, and who extracts the returns?
- **Insight**: Analyzes North-South capital flows and whether FDI represents development or extraction.

#### `education_debt.py` - Public Investment or Private Debt?
- **Left**: Government education spending across nations (bar chart)
- **Right**: Education spending trends (line chart, 1990-2023)
- **Question**: How nations fund education - and who pays the price?
- **Insight**: Compares public investment in education vs. privatization and student debt models.

#### `military_healthcare.py` - Guns vs Butter
- **Left**: Military spending as % of GDP (bar chart)
- **Right**: Military spending trends post-Cold War (line chart, 1990-2023)
- **Question**: Could military budgets fund universal healthcare?
- **Insight**: Examines resource allocation between security and social welfare.

#### `automation_unemployment.py` - Automation Without Liberation
- **Left**: Internet access by country (proxy for tech adoption) (bar chart)
- **Right**: Employment-to-population ratio over time (line chart, 1990-2023)
- **Question**: Has technology freed us from work or made it more precarious?
- **Insight**: Tests whether technological advancement has translated to shorter work weeks or more precarious employment.

### What Each Example Demonstrates

All examples demonstrate:
- Querying specific WDI indicators
- Creating paired indicator datasets or time series
- Building interactive charts with selection
- Creating filtered secondary visualizations
- Saving linked charts to HTML
- Using the new opinionated theme system

---

## Chart Theme and Styling

The package includes an opinionated design system inspired by modern data journalism (FiveThirtyEight, The Pudding, Our World in Data). All charts automatically use:

- **Custom color palette**: Distinctive 10-color scheme
- **Smart number formatting**: 
  - Currency as `$1.2M` not `1200000`
  - Percentages as `12.3` not `0.123`
  - Years as `2020` not `2,020.00`
- **Proper typography**: Modern font family with clear hierarchy
- **Centered titles and subtitles**: Professional presentation
- **Consistent interactions**: Selected items pop, deselected fade

The theme is centralized in `chart.py` so examples stay clean and focused on data analysis rather than styling.

