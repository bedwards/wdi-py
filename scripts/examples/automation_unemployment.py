"""Automation Without Liberation: Internet Access vs Employment.

Graeber argued technology could free us from work, yet we work more than ever.
As internet access (proxy for technology adoption) increases, has employment
become more precarious? Select countries to see employment trends.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import altair as alt

import wdi
from wdi.chart import ChartTheme, LineChartFiltered

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Compare developed and developing nations
countries = [
    "USA",  # United States
    "GBR",  # United Kingdom
    "DEU",  # Germany
    "FRA",  # France
    "JPN",  # Japan
    "KOR",  # South Korea
    "CHN",  # China
    "IND",  # India
    "BRA",  # Brazil
    "MEX",  # Mexico
    "ZAF",  # South Africa
    "NOR",  # Norway
    "SWE",  # Sweden
    "CAN",  # Canada
]

# Individuals using the Internet (% of population)
bar_indicator_code = "IT.NET.USER.ZS"
bar_indicator_name = wdi.sql.get_indicator_name(bar_indicator_code)

# Get internet usage as proxy for technological development
df_recent = wdi.df.get_indicator_data(
    indicator_code=bar_indicator_code,
    include_region=True,
    include_income_group=True,
)

df_recent = df_recent.filter(df_recent["country_code"].is_in(countries))
df_recent = wdi.df.filter_latest_year(df_recent)
df_recent = df_recent.filter(df_recent["value"].is_not_null())

print(f"Analyzing {len(df_recent)} countries' internet access")
print(f"Most recent year: {df_recent['year'].max()}")

# Create bar chart
chart = (
    alt.Chart(df_recent)
    .mark_bar(
        opacity=ChartTheme.BAR_OPACITY,
        cornerRadiusTopLeft=2,
        cornerRadiusTopRight=2,
    )
    .transform_calculate(value_pct="datum.value / 100")
    .encode(
        x=alt.X(
            "value_pct:Q",
            title=r"Internet Users (% of population)",
            axis=alt.Axis(
                format=ChartTheme.format_number("percent"),
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                gridColor=ChartTheme.GRID_COLOR,
            ),
        ),
        y=alt.Y(
            "country_name:N",
            title="Country",
            sort=alt.EncodingSortField(field="value", order="descending"),
            axis=alt.Axis(
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
            ),
        ),
        color=alt.Color(
            "country_name:N",
            scale=ChartTheme.get_color_scale(),
        ),
        tooltip=[
            alt.Tooltip("country_name:N", title="Country"),
            alt.Tooltip("income_group:N", title="Income"),
            alt.Tooltip("year:Q", format="d", title="Year"),
            alt.Tooltip("value_pct:Q", format=".0%", title="Internet use"),
        ],
    )
    .properties(
        width=550,
        height=500,
        title=ChartTheme.get_title_params(
            "Internet Access",
            "Most recent year (% of population) - Select to see labor force trends",
        ),
    )
)

brush = alt.selection_point(fields=["country_code"], name="brush")
chart = chart.add_params(brush).encode(
    opacity=alt.condition(brush, alt.value(ChartTheme.BAR_OPACITY), alt.value(0.3))
)

bar = chart

# Labor force participation rate, total (% of total population ages 15-64) (modeled ILO estimate)
ts_indicator_code = "SL.TLF.ACTI.ZS"

# Get employment-to-population ratio time series
# This shows what % of working-age population is employed
ts_df = wdi.df.get_time_series(
    indicator_code=[ts_indicator_code, bar_indicator_code],
    country_codes=countries,
    start_year=1990,
    end_year=2023,
    include_income_group=True,
)
ts_df = ts_df.with_columns(
    (ts_df["value"] / 100).alias("value_pct"),
    (ts_df["value_right"] / 100).alias("value_right_pct"),
)

ts_indicator_name = wdi.sql.get_indicator_name(ts_indicator_code)

ts_y_title = ts_indicator_name.split(",")[0].split("(")[0]
ts_title_prefix = " ".join(ts_y_title.split(" ")[:2])

# Create line chart
line = (
    LineChartFiltered(ts_df)
    .mark_wdi()
    .encode_wdi(
        x="year",
        y="value_pct",
        color="country_name",
        title=f"{ts_title_prefix} Over Time",
        subtitle=f"{ts_y_title}, selected countries (1990-2023)",
        x_title="Year",
        y_title=ts_indicator_name,
        y_format="percent",
        width=600,
        height=500,
        selection=brush,
        y2="value_right_pct",
        y2_title="Internet use",
    )
)

# Save linked charts
output_file = output_dir / "automation_unemployment.html"
wdi.chart.save_linked_charts(
    chart_left=bar,
    chart_right=line,
    filename=str(output_file),
    overall_title="Automation Without Liberation",
    overall_subtitle="Has technology freed us from work, or just made work more precarious?",
)

print(f"\n✓ Saved: {output_file}")
print("\nCritical questions:")
print("- As technology increases, has employment become more secure or less?")
print("- Why hasn't productivity translated to shorter work weeks?")
print("- Do some countries manage technological change better than others?")
print("- Has the digital economy created quality jobs or precarious 'gig work'?")
