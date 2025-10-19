"""The Education Trap: Public vs Private Spending.

David Graeber wrote about how education became a debt trap in the US.
Compare education spending patterns - who funds education publicly vs
forcing it onto individuals? Select countries to see spending trends.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import altair as alt

import wdi
from wdi.chart import ChartTheme

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Compare US with countries with different education funding models
countries = [
    "USA",  # United States - high private spending
    "NOR",  # Norway - high public spending
    "SWE",  # Sweden
    "DNK",  # Denmark
    "FIN",  # Finland
    "DEU",  # Germany
    "FRA",  # France
    "GBR",  # United Kingdom
    "CAN",  # Canada
    "AUS",  # Australia
    "JPN",  # Japan
    "KOR",  # South Korea
]

# Get government expenditure on education as % of GDP
df_recent = wdi.df.get_indicator_data(
    indicator_code="SE.XPD.TOTL.GD.ZS",  # Government expenditure on education (% of GDP)
    include_region=True,
    include_income_group=True,
)

df_recent = df_recent.filter(df_recent["country_code"].is_in(countries))
df_recent = wdi.df.filter_latest_year(df_recent)
df_recent = df_recent.filter(df_recent["value"].is_not_null())

print(f"Analyzing {len(df_recent)} countries' education spending")
print(f"Most recent year: {df_recent['year'].max()}")

# Create bar chart
# Around line 50-65, replace:

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
            title="Education Spending (% of GDP)",
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
            "Government Education Spending", "Most recent year (% of GDP) - Select to see trends"
        ),
    )
)

brush = alt.selection_point(fields=["country_code"], name="brush")
chart = chart.add_params(brush).encode(
    opacity=alt.condition(brush, alt.value(ChartTheme.BAR_OPACITY), alt.value(0.3))
)

bar = chart

# Get time series
ts_df = wdi.df.get_time_series(
    indicator_code="SE.XPD.TOTL.GD.ZS",
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
    title="Education Spending Trends",
    subtitle="Selected countries, 1990-2023",
    x_title="Year",
    y_title="Government Education Spending (% of GDP)",
    y_format="decimal",
    width=600,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "education_debt.html"
wdi.chart.save_linked_charts(
    chart_left=bar,
    chart_right=line,
    filename=str(output_file),
    overall_title="Public Investment or Private Debt?",
    overall_subtitle="How nations fund education - and who pays the price",
)

print(f"\n✓ Saved: {output_file}")
print("\nCritical questions:")
print("- Why does the US have lower public education spending than Nordic countries?")
print("- How does public spending correlate with student debt levels?")
print("- Has austerity reduced education investment over time?")
print("- Which model produces better educational outcomes?")
