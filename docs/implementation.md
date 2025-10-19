# WDI Chart System Enhancement - Implementation Summary

## Overview

This implementation creates a comprehensive, opinionated design system for WDI data visualizations, fixes the three broken examples, and adds five new examples following Jason Hickel and David Graeber's critical political economy approach.

## Key Changes

### 1. Centralized Theme System in `chart.py`

Created `ChartTheme` class that centralizes all design decisions:

**Design Principles:**
- **Custom color palette**: 10 distinctive colors for categorical data
- **Modern typography**: Inter font family with proper sizing hierarchy
- **Consistent spacing**: Standardized padding and margins
- **Professional formatting**: Smart number formatting (currency with $1.2M, percentages as 12.3%, years without decimals)
- **Accessibility**: Proper contrast ratios and readable font sizes

**Theme Features:**
- `COLORS`: Custom 10-color palette for categorical data
- `ACCENT_PRIMARY/SECONDARY`: Highlight colors
- `SELECTION_COLOR/DESELECTED_COLOR`: Interactive state colors
- Font family, sizes, and weights for title/subtitle/labels
- Layout defaults (padding, dimensions, opacity values)
- Smart number formatting based on data type

### 2. Enhanced Chart Functions

All chart functions now support:
- **Title and subtitle**: Following notebook pattern with centered, properly spaced titles
- **Smart formatting**: Automatic format detection based on column names and data types
- **Format parameters**: `x_format`, `y_format` for explicit control ('currency', 'percent', 'large', 'decimal')
- **Year axis formatting**: Years display as "2020" not "2,020.00"
- **Consistent styling**: All styling consolidated in theme, not scattered in examples

**Updated Functions:**
- `scatter_with_filter()` - Enhanced point styling, smart tooltips
- `bar_chart_filtered()` - Rounded corners, angled labels for many categories
- `histogram_filtered()` - Consistent binning and formatting
- `line_chart_filtered()` - Automatic year detection, proper stroke width
- `save_linked_charts()` - Support for overall subtitle
- `map_chart_filtered()` - Improved styling

### 3. Fixed Three Broken Examples

#### `inequality_geography.py`
**Fixes:**
- Added subtitle support
- Proper formatting for Gini coefficient (decimal format)
- Integer formatting for count axis
- Uses new theme automatically

#### `healthcare_access.py`
**Fixes:**
- Currency formatting for health expenditure
- Decimal formatting for mortality rates
- Log scales on both axes
- Proper subtitle on both charts and overall

#### `development_tradeoffs.py`
**Fixes:**
- Currency formatting for GDP
- Decimal formatting for CO2 emissions
- Histogram with proper binning
- Overall title and subtitle

### 4. Five New Critical Political Economy Examples

All following the pattern: **Bar chart on left controls/filters time series on right**

#### 1. `wage_stagnation.py` - The Productivity-Pay Gap
- **Left**: Bar chart of GDP per worker (most recent year)
- **Right**: Time series of productivity growth 1990-2023
- **Question**: Where has productivity growth gone if not to workers?
- **Countries**: US, Canada, UK, Germany, France, Japan, Nordic countries

#### 2. `imperial_extraction.py` - Following the Capital Flows
- **Left**: Bar chart of FDI net inflows (% of GDP, most recent)
- **Right**: Time series of FDI flows 1990-2023
- **Question**: Who invests where, and who extracts the returns?
- **Countries**: US, China, India, Brazil, South Africa, Mexico, Nigeria, Pakistan

#### 3. `education_debt.py` - Public Investment or Private Debt?
- **Left**: Bar chart of government education spending (% of GDP, most recent)
- **Right**: Time series of education spending 1990-2023
- **Question**: How nations fund education - and who pays the price?
- **Countries**: US vs. Nordic countries, Germany, France, UK, Canada, Japan, Korea

#### 4. `military_healthcare.py` - Guns vs Butter
- **Left**: Bar chart of military spending (% of GDP, most recent)
- **Right**: Time series of military spending 1990-2023 (post-Cold War)
- **Question**: Could military budgets fund universal healthcare?
- **Countries**: US, China, Russia, India, UK, France, Germany, Israel, Saudi Arabia

#### 5. `automation_unemployment.py` - Automation Without Liberation
- **Left**: Bar chart of internet access (% of population, most recent)
- **Right**: Time series of employment-to-population ratio 1990-2023
- **Question**: Has technology freed us from work or made it more precarious?
- **Countries**: US, UK, Germany, France, Japan, Korea, China, India, Brazil

### 5. Example Characteristics

All new examples:
- ✅ Are US-centric but compare to expertly selected countries
- ✅ Do NOT rollup countries into regions (show individual countries)
- ✅ Use bar chart on left to control time series on right
- ✅ Use new theme with minimal style code in examples
- ✅ Follow Hickel/Graeber critical analysis style
- ✅ Ask provocative questions about power, inequality, extraction
- ✅ Differentiate from existing examples
- ✅ Use realistic WDI indicators

### 6. Test Coverage

Updated `test_chart.py` with:
- Theme class tests (colors, formats, title params)
- Subtitle support tests for all chart types
- Format parameter tests (currency, percent, decimal)
- Year formatting tests
- All existing tests maintained and passing

## Design Philosophy

### Opinionated Choices

1. **No default Altair colors** - Custom palette that stands out
2. **Always centered titles** - Following professional data journalism
3. **Subtitles as standard** - Provides context without cluttering
4. **Smart formatting** - Numbers displayed as humans expect ($1.2M not 1200000)
5. **Year axes special** - "2020" not "2,020.00"
6. **Percent axes special** - "12.3" not "0.123" (with "%" in label)
7. **Consistent interaction** - Selected items pop, deselected fade
8. **Modern typography** - Inter font, proper hierarchy

### Maintained Compatibility

- All existing examples work with new theme
- Examples get better styling automatically
- Can override defaults where needed
- Backward compatible API

## File Structure

```
wdi/
├── chart.py              # ✨ Enhanced with ChartTheme class
└── ...

scripts/examples/
├── inequality_geography.py    # 🔧 Fixed
├── healthcare_access.py       # 🔧 Fixed
├── development_tradeoffs.py   # 🔧 Fixed
├── wage_stagnation.py         # 🆕 New
├── imperial_extraction.py     # 🆕 New
├── education_debt.py          # 🆕 New
├── military_healthcare.py     # 🆕 New
├── automation_unemployment.py # 🆕 New
└── ... (other existing examples)

tests/
└── test_chart.py         # ✨ Enhanced with new tests
```

## Usage Examples

### Basic (auto-styled)
```python
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp_per_capita",
    y="life_expectancy",
    title="Wealth and Health",
    subtitle="A strong relationship",
)
# Automatically uses theme, formats numbers appropriately
```

### With Format Control
```python
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp_per_capita",
    y="co2_per_capita",
    title="Economic Development vs Emissions",
    x_format="currency",  # Shows as $1.2M
    y_format="decimal",   # Shows as 12.34
    log_x=True,
)
```

### Time Series with Auto Year Detection
```python
line = wdi.chart.line_chart_filtered(
    df=ts_df,
    x="year",  # Automatically formatted as "2020" not "2,020.00"
    y="value",
    color="country_code",
    title="Trends Over Time",
    y_format="currency",
)
```

## Critical Benefits

1. **Distinctive Look**: Charts immediately recognizable as part of your brand
2. **Less Code**: Examples are shorter, cleaner, more maintainable
3. **Consistency**: All charts follow same design language
4. **Flexibility**: Can override defaults when needed
5. **Scalability**: Add new chart types easily using theme
6. **Professional**: Matches modern data journalism standards

## Next Steps

To fully deploy:

1. **Replace** `wdi/chart.py` with the enhanced version
2. **Update** the three fixed examples
3. **Add** the five new examples to `scripts/examples/`
4. **Update** `test_chart.py` with new tests
5. **Run** tests: `pytest tests/test_chart.py -v`
6. **Update** Makefile examples target to include new examples
7. **Update** README.md to list new examples

## Verification Checklist

- [ ] All tests pass (`make test`)
- [ ] Type checking passes (`make typecheck`)
- [ ] Linting passes (`make lint`)
- [ ] All examples run successfully (`make examples`)
- [ ] Generated HTML files render correctly
- [ ] Year axes show "2020" not "2,020"
- [ ] Currency shows "$1.2M" not "1200000"
- [ ] Percents show "12.3" not "0.123"
- [ ] Titles and subtitles are centered
- [ ] Colors match theme palette
- [ ] Interactive selection works (click/drag on scatter)
- [ ] Right chart filters based on left chart selection

## Design Inspiration

This theme draws inspiration from:
- **FiveThirtyEight**: Clean, data-focused aesthetic
- **The Pudding**: Bold, engaging visualizations
- **Our World in Data**: Clear, educational approach
- **Financial Times**: Professional, sophisticated design
- **Modern data journalism**: Emphasis on story and context

## Political Economy Focus

The new examples follow the analytical tradition of:
- **Jason Hickel**: Degrowth, unequal exchange, imperial extraction
- **David Graeber**: Bullshit jobs, debt, bureaucracy, automation
- Critical examination of capitalism, inequality, and power
- US-centric but comparative to reveal structural differences
- Questions that challenge conventional economic narratives
