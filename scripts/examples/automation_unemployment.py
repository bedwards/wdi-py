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
from wdi.chart import ChartTheme

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

# Get internet usage as proxy for technological development
df_recent = wdi.df.get_indicator_data(
    indicator_code="IT.NET.USER.ZS",  # Individuals using the Internet (% of population)
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
            title="Internet Users (% of population)",
            axis=alt.Axis(
                format=ChartTheme.format_number("decimal"),
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                gridColor=ChartTheme.GRID_COLOR,
            ),
        ),
        color=alt.Color(
            "income_group:N",
            scale=ChartTheme.get_color_scale(),
            legend=alt.Legend(
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                labelFontSize=ChartTheme.LABEL_FONT_SIZE,
            ),
        ),
        tooltip=[
            alt.Tooltip("country_name:N"),
            alt.Tooltip("value:Q", format=".1f"),
            alt.Tooltip("year:Q", format="d"),
            alt.Tooltip("income_group:N"),
        ],
    )
    .properties(
        width=550,
        height=500,
        title=ChartTheme.get_title_params(
            "Internet Access",
            "Most recent year (% of population) - Select to see employment trends",
        ),
    )
)

brush = alt.selection_point(fields=["country_code"], name="brush")
chart = chart.add_params(brush).encode(
    opacity=alt.condition(brush, alt.value(ChartTheme.BAR_OPACITY), alt.value(0.3))
)

bar = chart

# Get employment-to-population ratio time series
# This shows what % of working-age population is employed
ts_df = wdi.df.get_time_series(
    indicator_code="SL.EMP.TOTL.SP.ZS",  # Employment to population ratio (%)
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
    title="Employment Rates Over Time",
    subtitle="Employment-to-population ratio, selected countries (1990-2023)",
    x_title="Year",
    y_title="Employment to Population Ratio (%)",
    y_format="decimal",
    width=600,
    height=500,
    selection=brush,
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
