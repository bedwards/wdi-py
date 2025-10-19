"""Imperial Extraction: Foreign Direct Investment Flows.

Jason Hickel argues wealthy nations extract value from the Global South
through unequal exchange. Examine net FDI flows - who invests where, and
who extracts the returns? Select countries to see their FDI trends.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Compare US with major economies and key Global South nations
countries = [
    "USA",  # United States
    "CHN",  # China
    "IND",  # India
    "BRA",  # Brazil
    "ZAF",  # South Africa
    "MEX",  # Mexico
    "NGA",  # Nigeria
    "PAK",  # Pakistan
    "BGD",  # Bangladesh
    "VNM",  # Vietnam
    "GBR",  # United Kingdom
    "FRA",  # France
]

# Get most recent FDI net inflows as % of GDP
df_recent = wdi.df.get_indicator_data(
    indicator_code="BX.KLT.DINV.WD.GD.ZS",  # Foreign direct investment, net inflows (% of GDP)
    include_region=True,
    include_income_group=True,
)

df_recent = df_recent.filter(df_recent["country_code"].is_in(countries))
df_recent = wdi.df.filter_latest_year(df_recent)
df_recent = df_recent.filter(df_recent["value"].is_not_null())

print(f"Analyzing {len(df_recent)} countries' FDI patterns")
print(f"Most recent year: {df_recent['year'].max()}")

# Create bar chart showing most recent FDI inflows
bar, brush = wdi.chart.scatter_with_filter(
    df=df_recent,
    x="country_name",
    y="value",
    color="income_group",
    tooltip=["country_name", "value", "year", "income_group"],
    title="Foreign Direct Investment Net Inflows",
    subtitle="Most recent year (% of GDP) - Select to see trends",
    x_title="Country",
    y_title="FDI Net Inflows (% of GDP)",
    y_format="decimal",
    width=550,
    height=500,
)

# Get time series
ts_df = wdi.df.get_time_series(
    indicator_code="BX.KLT.DINV.WD.GD.ZS",
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
    title="FDI Flows Over Time",
    subtitle="Selected countries, 1990-2023",
    x_title="Year",
    y_title="FDI Net Inflows (% of GDP)",
    y_format="decimal",
    width=600,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "imperial_extraction.html"
wdi.chart.save_linked_charts(
    chart_left=bar,
    chart_right=line,
    filename=str(output_file),
    overall_title="Following the Capital Flows",
    overall_subtitle="Who invests where, and who extracts the returns?",
)

print(f"\n✓ Saved: {output_file}")
print("\nCritical questions:")
print("- Do high FDI inflows indicate development opportunity or extraction?")
print("- How do net flows compare to profit repatriation?")
print("- Which countries are capital exporters vs. recipients?")
print("- Has China disrupted traditional North-South investment patterns?")
