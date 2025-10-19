"""Guns vs Butter: Military Spending vs Healthcare.

A classic tradeoff: the US spends more on military than the next several
countries combined, yet lacks universal healthcare. Compare military
spending across nations. Select countries to see spending trends over time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import altair as alt

import wdi
from wdi.chart import ChartTheme

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

# Around line 55-65, replace:

chart = (
    alt.Chart(df_recent)
    .mark_bar(
        opacity=ChartTheme.BAR_OPACITY,
        cornerRadiusTopLeft=2,
        cornerRadiusTopRight=2,
    )
    .encode(
        y=alt.Y(
            "country_name:N",
            title="Country",
            sort=alt.EncodingSortField(field="value", order="descending"),
            axis=alt.Axis(
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
            ),
        ),
        x=alt.X(
            "value:Q",
            title="Military Expenditure (% of GDP)",
            axis=alt.Axis(
                format=ChartTheme.format_number("decimal"),
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                gridColor=ChartTheme.GRID_COLOR,
            ),
        ),
        color=alt.Color(
            "country_code:N",
            scale=ChartTheme.get_color_scale(),
            legend=None,
        ),
        tooltip=[
            alt.Tooltip("country_name:N"),
            alt.Tooltip("value:Q", format=".2f"),
            alt.Tooltip("year:Q", format="d"),
        ],
    )
    .properties(
        width=550,
        height=500,
        title=ChartTheme.get_title_params(
            "Military Spending", "Most recent year (% of GDP) - Select to see trends"
        ),
    )
)

brush = alt.selection_point(fields=["country_code"], name="brush")
chart = chart.add_params(brush).encode(
    opacity=alt.condition(brush, alt.value(ChartTheme.BAR_OPACITY), alt.value(0.3))
)

bar = chart

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
