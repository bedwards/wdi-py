# WDI Chart Theme - Quick Reference Guide

## Philosophy

> "Opinionated but flexible, distinctive but professional"

The theme makes strong design choices so your charts look polished by default, but allows overrides when needed.

## Key Design Decisions

### 1. Number Formatting

The theme automatically formats numbers based on type:

| Format Type | Example Output | Use For |
|------------|----------------|---------|
| `currency` | `$1.2M`, `$345.6k` | GDP, income, spending |
| `percent` | `12.3` | Rates, percentages (% in axis label) |
| `large` | `1.2M`, `345.6k` | Population, counts |
| `decimal` | `12.34` | Ratios, coefficients |
| `integer` | `1234` | Whole number counts |
| `default` | `1,234` | Generic numbers |

**Years are special**: Always formatted as `2020` never `2,020.00`

### 2. Typography Hierarchy

```
Title:    16px, weight 600 (semibold)
Subtitle: 13px, weight 400 (regular), gray color
Labels:   11px
```

All text uses Inter font family (with system fallbacks)

### 3. Colors

**Categorical Data (10 colors):**
```python
#1f77b4  # Steel blue
#ff7f0e  # Vibrant orange  
#2ca02c  # Forest green
#d62728  # Crimson
#9467bd  # Purple
#8c564b  # Brown
#e377c2  # Pink
#7f7f7f  # Gray
#bcbd22  # Olive
#17becf  # Cyan
```

**Accent Colors:**
- Primary: `#ff6b6b` (coral red)
- Secondary: `#4ecdc4` (turquoise)

**Interactive States:**
- Selected: `#2d3748` (dark slate)
- Deselected: `#e2e8f0` (light gray, 30% opacity)

### 4. Layout

- Background: White (`#ffffff`)
- Grid: Light gray (`#f1f5f9`)
- Default padding: 20px
- Default size: 500x400 (left chart), 450x400 (right chart)

## Usage Examples

### Basic Usage (Auto-styling)

```python
# Theme applies automatically
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp_per_capita",
    y="life_expectancy",
    title="Wealth and Health"
)
```

### With Subtitle

```python
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp",
    y="emissions",
    title="Economic Development",
    subtitle="GDP vs CO2 emissions across nations"
)
```

### Explicit Format Control

```python
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp_per_capita",
    y="co2_per_capita",
    x_format="currency",  # $1.2M
    y_format="decimal",   # 12.34
)
```

### Time Series with Year

```python
# Years auto-detected and formatted as "2020"
line = wdi.chart.line_chart_filtered(
    df=ts_df,
    x="year",  
    y="value",
    y_format="currency",
)
```

### Bar Chart with Count

```python
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="region",
    y="count()",
    y_format="integer",  # Whole numbers
    title="Regional Distribution",
    subtitle="Number of countries by region"
)
```

### Overall Titles

```python
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename="output.html",
    overall_title="Main Title Here",
    overall_subtitle="Supporting context here"
)
```

## Format Detection

The theme tries to auto-detect appropriate formatting:

```python
# If column name contains:
"gdp", "income", "capita" → currency format
"percent", "rate" → percent format  
"year" → year format (no decimals/commas)

# Otherwise uses default
```

## Customizing the Theme

### Override Individual Properties

```python
from wdi.chart import ChartTheme

# Use custom colors for a specific chart
custom_scale = alt.Scale(range=["#ff0000", "#00ff00", "#0000ff"])

scatter = alt.Chart(df).mark_point().encode(
    x="x_value",
    y="y_value", 
    color=alt.Color("category", scale=custom_scale)
)
```

### Access Theme Constants

```python
from wdi.chart import ChartTheme

# Use theme colors in custom charts
my_color = ChartTheme.COLORS[0]
my_accent = ChartTheme.ACCENT_PRIMARY

# Use theme formatting
currency_fmt = ChartTheme.format_number("currency")
year_fmt = ChartTheme.format_axis_year()
```

### Create Custom Title

```python
from wdi.chart import ChartTheme

title = ChartTheme.get_title_params(
    "My Custom Title",
    "With a subtitle"
)

chart = alt.Chart(df).mark_bar().properties(title=title)
```

## Best Practices

### DO:
✅ Use subtitles to provide context  
✅ Let the theme handle formatting automatically  
✅ Use `x_format` and `y_format` when auto-detection isn't right  
✅ Keep titles concise and descriptive  
✅ Use color meaningfully (by category, not decoration)  
✅ Test with actual data to ensure tooltips work well

### DON'T:
❌ Hardcode colors in examples (use theme)  
❌ Override formatting unless necessary  
❌ Create titles without subtitles for complex charts  
❌ Use ALL CAPS in titles  
❌ Format years with decimals (theme handles this)  
❌ Display raw percentages as 0.123 instead of 12.3

## Common Patterns

### Pattern 1: Scatter Plot + Bar Chart (Regional Distribution)

```python
# Left: Scatter with selection
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="value",
    y="country_name",
    color="region",
    title="Main Analysis",
    subtitle="Select countries to filter",
    width=500,
    height=600
)

# Right: Bar chart filtered by selection
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="region",
    y="count()",
    color="region",
    title="Regional Distribution",
    subtitle="Selected countries",
    width=450,
    height=600,
    selection=brush
)
```

### Pattern 2: Bar Chart + Time Series

```python
# Left: Bar chart with selection (recent year)
bar, brush = wdi.chart.scatter_with_filter(
    df=df_recent,
    x="country_name",
    y="value",
    color="country_code",
    title="Current Values",
    subtitle="Select to see trends",
    y_format="currency",
    width=550,
    height=500
)

# Right: Time series filtered by selection
line = wdi.chart.line_chart_filtered(
    df=ts_df,
    x="year",
    y="value",
    color="country_code",
    title="Trends Over Time",
    subtitle="Selected countries (1990-2023)",
    y_format="currency",
    width=600,
    height=500,
    selection=brush
)
```

### Pattern 3: Scatter Plot + Histogram

```python
# Left: Scatter with log scale
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="gdp_per_capita",
    y="life_expectancy",
    color="region",
    title="Development Indicators",
    x_format="currency",
    log_x=True,
    width=500,
    height=500
)

# Right: Distribution of selected points
hist = wdi.chart.histogram_filtered(
    df=df,
    column="life_expectancy",
    bins=30,
    title="Life Expectancy Distribution",
    subtitle="Selected countries",
    x_format="decimal",
    width=450,
    height=500,
    selection=brush
)
```

## Troubleshooting

### Years showing as "2,020.00"
**Solution**: Make sure column is named with "year" in it, or the theme will auto-detect and format correctly.

```python
# Good - auto-detected
df = pl.DataFrame({"year": [2020, 2021], "value": [100, 110]})

# Also good - explicit format
line = wdi.chart.line_chart_filtered(
    df=df,
    x="time_period",  # not detected as year
    y="value",
    # Let Altair handle as quantitative, then format axis
)
```

### Numbers not formatting as currency
**Solution**: Use explicit `x_format` or `y_format` parameter:

```python
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="spending",  # won't auto-detect as currency
    y="outcomes",
    x_format="currency",  # explicit
)
```

### Colors look wrong
**Solution**: Check if you're overriding the theme inadvertently:

```python
# Wrong - hardcoded color
color=alt.value("steelblue")

# Right - use theme
color=alt.Color("region:N", scale=ChartTheme.get_color_scale())

# Or just let the chart function handle it
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x",
    y="y",
    color="region"  # Theme applied automatically
)
```

### Titles not centered
**Solution**: Use the chart functions, not raw Altair. The functions apply theme automatically:

```python
# Wrong - manual Altair
chart = alt.Chart(df).mark_bar().properties(title="My Title")

# Right - use wdi.chart functions
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="category",
    y="count()",
    title="My Title",
    subtitle="Context here"
)
```

## Theme Maintenance

The theme is defined in one place: `wdi/chart.py` in the `ChartTheme` class.

To modify the theme globally:

1. Edit `ChartTheme` class constants
2. All charts automatically use new values
3. No need to update individual examples

Example - changing primary accent color:

```python
# In chart.py
class ChartTheme:
    ACCENT_PRIMARY = "#your_new_color"  # Change here
    # All charts now use new color
```

## Migration from Old Examples

If you have old examples without the theme:

### Before (old style):
```python
chart = (
    alt.Chart(df)
    .mark_circle(size=60, opacity=0.7)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(type="log")),
        y=alt.Y("y:Q"),
        color=alt.condition(
            brush,
            "region:N",
            alt.value("lightgray")
        ),
        tooltip=["country", "x", "y"]
    )
    .properties(width=400, height=400, title="My Chart")
    .add_params(brush)
)
```

### After (new style):
```python
chart, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x",
    y="y",
    color="region",
    tooltip=["country", "x", "y"],
    title="My Chart",
    subtitle="Additional context",
    log_x=True,
    width=400,
    height=400
)
# Much cleaner! Theme handles all styling.
```

## Quick Reference Table

| Task | Function | Key Parameters |
|------|----------|----------------|
| Scatter with selection | `scatter_with_filter()` | `x`, `y`, `color`, `log_x`, `log_y`, `x_format`, `y_format` |
| Bar chart | `bar_chart_filtered()` | `x`, `y`, `color`, `selection`, `y_format` |
| Histogram | `histogram_filtered()` | `column`, `bins`, `selection`, `x_format` |
| Time series | `line_chart_filtered()` | `x`, `y`, `color`, `selection`, `y_format` |
| Save charts | `save_linked_charts()` | `chart_left`, `chart_right`, `filename`, `overall_title`, `overall_subtitle` |
| Map | `map_chart_filtered()` | `country_col`, `value_col`, `selection` |

## Format Type Reference

| Data Type | Recommended Format | Example |
|-----------|-------------------|---------|
| GDP, income, spending | `currency` | $1.2M |
| Population, emissions | `large` | 1.2M |
| Gini, ratios | `decimal` | 0.42 |
| Rates (unemployment) | `percent` | 5.3 |
| Year | (auto) | 2020 |
| Count | `integer` | 1,234 |
| Generic | `default` | 1,234 |

## Resources

- **Altair docs**: https://altair-viz.github.io/
- **Vega-Lite**: https://vega.github.io/vega-lite/
- **Color advice**: https://colorbrewer2.org/
- **Typography**: https://fonts.google.com/specimen/Inter

## Examples Gallery

See all examples in action:
```bash
make examples-all
open data/output/*.html
```

Key examples demonstrating theme:
- `inequality_geography.html` - Scatter + bar pattern
- `wage_stagnation.html` - Bar + time series pattern  
- `healthcare_access.html` - Log scales, currency formatting
- `development_tradeoffs.html` - Histogram pattern
- `automation_unemployment.html` - Employment rates over time
