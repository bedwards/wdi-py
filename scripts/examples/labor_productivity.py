"""Labor Time and Economic Output.

Examine the relationship between working hours and GDP per capita.
Do people in wealthier countries work fewer hours? Select countries
to see the trend over time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi
import polars as pl

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get employment-to-population ratio as a proxy for labor intensity
# and GDP per capita for 2019
df = wdi.df.get_indicator_pairs(
    indicator_x="SL.EMP.TOTL.SP.ZS",  # Employment to population ratio
    indicator_y="NY.GDP.PCAP.CD",      # GDP per capita
    year=2019,
    include_region=True,
    include_income_group=True,
)

# Remove nulls
df = df.filter(
    df["x_value"].is_not_null() & df["y_value"].is_not_null()
)

print(f"Analyzing {len(df)} countries with employment and GDP data for 2019")

# Create scatter plot
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="income_group",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="Employment Rate vs GDP per Capita (2019)",
    x_title="Employment to Population Ratio (%)",
    y_title="GDP per Capita (US$, log scale)",
    log_y=True,
    width=500,
    height=500,
)

# Get time series data for selected countries
# For the filtered chart, we'll show regional patterns
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="region",
    y="count()",
    color="region",
    title="Regional Distribution (Selected Countries)",
    x_title="Region",
    y_title="Number of Countries",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "labor_productivity.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="Labor and Wealth: Select countries to explore employment patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Do wealthier countries have lower employment rates?")
print("- What explains high-GDP countries with high employment?")
print("- Are there regional patterns in the labor-wealth relationship?")
