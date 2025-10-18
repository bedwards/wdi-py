"""External Debt and Development.

Investigate how external debt burdens relate to economic growth.
Are heavily indebted countries trapped in low growth? Select countries
to see how debt levels vary by region.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get external debt and GDP growth rate
df = wdi.df.get_indicator_pairs(
    indicator_x="DT.DOD.DECT.GN.ZS",  # External debt stocks (% of GNI)
    indicator_y="NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    year=2020,
    include_region=True,
    include_income_group=True,
)

# Remove nulls and extreme outliers
df = df.filter(
    df["x_value"].is_not_null() & 
    df["y_value"].is_not_null() &
    (df["x_value"] < 300)  # Remove extreme debt outliers
)

print(f"Analyzing {len(df)} countries with debt and growth data for 2020")

# Create scatter plot
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="income_group",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="External Debt vs GDP Growth (2020)",
    x_title="External Debt (% of GNI)",
    y_title="GDP Growth Rate (%)",
    width=500,
    height=500,
)

# Create bar chart showing regional distribution
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
output_file = output_dir / "debt_development.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="The Debt Burden: Select countries to explore regional debt patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Is high debt associated with low or negative growth?")
print("- Which regions have the highest debt burdens?")
print("- Are there countries with high debt but positive growth?")
