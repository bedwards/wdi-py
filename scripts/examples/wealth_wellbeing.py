"""Wealth and Wellbeing.

Does more wealth equal better health outcomes? Explore GDP per capita
against life expectancy. Select countries to see their income group
distribution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get GDP per capita and life expectancy
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita
    indicator_y="SP.DYN.LE00.IN",  # Life expectancy at birth
    year=2021,
    include_region=True,
    include_income_group=True,
)

# Remove nulls
df = df.filter(df["x_value"].is_not_null() & df["y_value"].is_not_null())

print(f"Analyzing {len(df)} countries with GDP and life expectancy data for 2021")

# Create scatter plot
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="region",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="GDP per Capita vs Life Expectancy (2021)",
    x_title="GDP per Capita (US$, log scale)",
    y_title="Life Expectancy (years)",
    log_x=True,
    width=500,
    height=500,
)

# Create bar chart of income groups for selected countries
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="income_group",
    y="count()",
    color="income_group",
    title="Income Group Distribution (Selected Countries)",
    x_title="Income Group",
    y_title="Number of Countries",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "wealth_wellbeing.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="Beyond GDP: Select countries to explore the wealth-health relationship",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Do diminishing returns set in for life expectancy gains?")
print("- Which countries achieve high life expectancy despite modest GDP?")
print("- What role does inequality play in the outliers?")
