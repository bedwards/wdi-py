"""Inequality and Geographic Distribution.

Explore how income inequality (Gini coefficient) varies across regions.
Click and drag on the scatter plot to select countries and see their
regional distribution in the bar chart.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

# Ensure output directory exists
output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get Gini coefficient data with regional information
df = wdi.df.get_indicator_data(
    indicator_code="SI.POV.GINI",  # Gini index
    include_region=True,
    include_income_group=True,
)

# Filter to most recent year per country
df = wdi.df.filter_latest_year(df)

# Remove null values
df = df.filter(df["value"].is_not_null())

print(f"Analyzing {len(df)} countries with Gini coefficient data")
print(f"Years covered: {df['year'].min()} - {df['year'].max()}")

# Create scatter plot: Gini coefficient by country with selection
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="value",
    y="country_name",
    color="region",
    tooltip=["country_name", "value", "year", "region", "income_group"],
    title="Income Inequality by Country (Gini Coefficient)",
    x_title="Gini Coefficient (higher = more unequal)",
    y_title="Country",
    width=500,
    height=600,
)

# Create bar chart showing regional distribution of selected countries
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="region",
    y="count()",
    color="region",
    title="Regional Distribution of Selected Countries",
    x_title="Region",
    y_title="Number of Countries",
    width=450,
    height=600,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "inequality_geography.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="Global Income Inequality: Select countries to explore regional patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nInsights to explore:")
print("- Which regions have the highest concentration of unequal countries?")
print("- Are high-inequality countries clustered geographically?")
print("- How does inequality vary within regions?")
