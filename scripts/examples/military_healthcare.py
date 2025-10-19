"""Guns vs Butter: Military Spending vs Healthcare.

A classic tradeoff: the US spends more on military than the next several
countries combined, yet lacks universal healthcare. Compare military
spending across nations. Select countries to see spending trends over time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Compare major military spenders and some smaller nations
countries = [
    "USA",  # United States - highest absolute spending
    "CHN",  # China
    "RUS",  # Russia
    "IND",  # India
    "GBR",  # United Kingdom
    "FRA",  # France
    "DEU",  # Germany
    "JPN",  # Japan
    "KOR",  # South Korea
    "ISR",  # Israel
    "SAU",  # Saudi Arabia
    "CAN",  # Canada
    "NOR",  # Norway
    "SWE",  # Sweden
    "CHE",  # Switzerland
]

# Get military expenditure as % of GDP
df_recent = wdi.df.get_indicator_data(
    indicator_code="MS.MIL.XPND.GD.ZS",  # Military expenditure (% of GDP)
    include_region=True,
    include_income_group=True,
)

df_recent = df_recent.filter(df_recent["country_code"].is_in(countries))
df_recent = wdi.df.filter_latest_year(df_recent)
df_recent = df_recent.filter(df_recent["value"].is_not_null())

print(f"Analyzing {len(df_recent)} countries' military spending")
print(f"Most recent year: {df_recent['year'].max()}")

# Create bar chart
bar, brush = wdi.chart.scatter_with_filter(
    df=df_recent,
    x="country_name",
    y="value",
    color="country_code",
    tooltip=["country_name", "value", "year"],
    title="Military Spending",
    subtitle="Most recent year (% of GDP) - Select to see trends",
    x_title="Country",
    y_title="Military Expenditure (% of GDP)",
    y_format="decimal",
    width=550,
    height=500,
)

# Get time series since 1990 (post-Cold War)
ts_df = wdi.df.get_time_series(
    indicator_code="MS.MIL.XPND.GD.ZS",
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
    title="Military Spending Over Time",
    subtitle="Selected countries, post-Cold War (1990-2023)",
    x_title="Year",
    y_title="Military Expenditure (% of GDP)",
    y_format="decimal",
    width=600,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "military_healthcare.html"
wdi.chart.save_linked_charts(
    chart_left=bar,
    chart_right=line,
    filename=str(output_file),
    overall_title="Guns vs Butter",
    overall_subtitle="How nations allocate resources between security and welfare",
)

print(f"\n✓ Saved: {output_file}")
print("\nCritical questions:")
print("- Has the post-Cold War 'peace dividend' materialized?")
print("- How does US military spending compare to social spending?")
print("- Which countries reduced military spending after the Cold War?")
print("- Could military budgets fund universal healthcare?")
