"""Wage Stagnation and Declining Labor Share.

The US has seen decades of wage stagnation despite productivity growth.
Compare the labor share of income across wealthy nations over time.
Select countries to see how workers' share of national income has evolved.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Compare wealthy nations plus some developing for context
countries = [
    "USA",  # United States
    "CAN",  # Canada
    "GBR",  # United Kingdom
    "DEU",  # Germany
    "FRA",  # France
    "JPN",  # Japan
    "AUS",  # Australia
    "SWE",  # Sweden
    "NOR",  # Norway
    "DNK",  # Denmark
    "CHE",  # Switzerland
    "NLD",  # Netherlands
]

# Get most recent labor share data for bar chart
df_recent = wdi.df.get_indicator_data(
    indicator_code="SL.GDP.PCAP.EM.KD",  # GDP per person employed (proxy for productivity)
    include_region=True,
    include_income_group=True,
)

# Filter to our countries and get most recent
df_recent = df_recent.filter(df_recent["country_code"].is_in(countries))
df_recent = wdi.df.filter_latest_year(df_recent)
df_recent = df_recent.filter(df_recent["value"].is_not_null())

print(f"Analyzing {len(df_recent)} wealthy nations")
print(f"Most recent year: {df_recent['year'].max()}")

# Create bar chart with selection
bar, brush = wdi.chart.scatter_with_filter(
    df=df_recent,
    x="country_name",
    y="value",
    color="country_code",
    tooltip=["country_name", "value", "year"],
    title="GDP per Worker (Most Recent)",
    subtitle="Select countries to compare trends over time",
    x_title="Country",
    y_title="GDP per Person Employed (constant 2017 PPP $)",
    y_format="currency",
    width=500,
    height=500,
)

# Get time series for labor compensation share
# Using wage and salaried workers as proxy since labor share isn't directly available
ts_df = wdi.df.get_time_series(
    indicator_code="SL.GDP.PCAP.EM.KD",
    country_codes=countries,
    start_year=1990,
    end_year=2023,
)

# Create line chart
line = wdi.chart.line_chart_filtered(
    df=ts_df,
    x="year",
    y="value",
    color="country_code",
    title="Productivity Growth Over Time",
    subtitle="GDP per worker, 1990-2023 (selected countries)",
    x_title="Year",
    y_title="GDP per Person Employed (constant 2017 PPP $)",
    y_format="currency",
    width=600,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "wage_stagnation.html"
wdi.chart.save_linked_charts(
    chart_left=bar,
    chart_right=line,
    filename=str(output_file),
    overall_title="The Productivity-Pay Gap",
    overall_subtitle="Has worker productivity growth translated to wage growth?",
)

print(f"\n✓ Saved: {output_file}")
print("\nCritical questions:")
print("- Where has productivity growth gone if not to workers?")
print("- Which countries maintain stronger connections between productivity and wages?")
print("- How does the US compare to social democracies in Europe?")
