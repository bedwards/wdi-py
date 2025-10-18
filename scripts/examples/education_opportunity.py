"""Education and Economic Opportunity.

Explore the relationship between educational attainment and unemployment.
Does more education guarantee economic security? Select countries to see
patterns within income groups.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get school enrollment (secondary) and unemployment rate
df = wdi.df.get_indicator_pairs(
    indicator_x="SE.SEC.ENRR",        # School enrollment, secondary (% gross)
    indicator_y="SL.UEM.TOTL.ZS",     # Unemployment, total (% of labor force)
    year=2020,
    include_region=True,
    include_income_group=True,
)

# Remove nulls
df = df.filter(
    df["x_value"].is_not_null() & df["y_value"].is_not_null()
)

print(f"Analyzing {len(df)} countries with education and unemployment data for 2020")

# Create scatter plot
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="region",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="Secondary School Enrollment vs Unemployment (2020)",
    x_title="Secondary School Enrollment (% gross)",
    y_title="Unemployment Rate (%)",
    width=500,
    height=500,
)

# Create bar chart showing income groups of selected countries
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="income_group",
    y="count()",
    color="income_group",
    title="Income Distribution (Selected Countries)",
    x_title="Income Group",
    y_title="Number of Countries",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "education_opportunity.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="The Education Paradox: Select countries to explore enrollment-employment patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Does higher enrollment correlate with lower unemployment?")
print("- Which countries have high education but high unemployment?")
print("- How do income groups cluster in this relationship?")
