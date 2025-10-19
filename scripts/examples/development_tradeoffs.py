"""Development and Environmental Tradeoffs.

Examine the relationship between economic growth (GDP per capita) and
environmental impact (CO2 emissions per capita). Select countries on the
scatter plot to see their emission distribution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get GDP per capita and CO2 emissions for 2019 (pre-pandemic)
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita (current US$)
    indicator_y="EN.ATM.CO2E.PC",  # CO2 emissions (metric tons per capita)
    year=2019,
    include_region=True,
    include_income_group=True,
)

# Remove nulls
df = df.filter(df["x_value"].is_not_null() & df["y_value"].is_not_null())

print(f"Analyzing {len(df)} countries with GDP and CO2 data for 2019")

# Create scatter plot with logarithmic x-axis
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="income_group",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="Economic Development vs Carbon Emissions (2019)",
    subtitle="The environmental cost of prosperity",
    x_title="GDP per Capita (US$, log scale)",
    y_title="CO2 Emissions per Capita (metric tons)",
    x_format="currency",
    y_format="decimal",
    log_x=True,
    width=500,
    height=500,
)

# Create histogram of CO2 emissions for selected countries
histogram = wdi.chart.histogram_filtered(
    df=df,
    column="y_value",
    bins=30,
    title="Distribution of CO2 Emissions",
    subtitle="Selected countries",
    x_title="CO2 per Capita (metric tons)",
    x_format="decimal",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "development_tradeoffs.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=histogram,
    filename=str(output_file),
    overall_title="The Carbon Cost of Development",
    overall_subtitle="Select countries to examine emission patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Is there a decoupling of wealth and emissions in high-income countries?")
print("- Which low-GDP countries have disproportionately high emissions?")
print("- What does the distribution tell us about global inequality in emissions?")
