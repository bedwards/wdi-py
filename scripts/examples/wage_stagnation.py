"""Wage Stagnation and Declining Labor Share.

The US has seen decades of wage stagnation despite productivity growth.
Compare the labor share of income across wealthy nations over time.
Select countries to see how workers' share of national income has evolved.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import altair as alt

import wdi
from wdi.chart import ChartTheme

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

# Create bar chart showing most recent gdp per worker
# Use scatter plot positioned vertically to show bars
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
            title="GDP per Person Employed (constant 2017 PPP $)",
            axis=alt.Axis(
                format=ChartTheme.format_number("currency"),
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
            alt.Tooltip("country_name:N", title="Country"),
            alt.Tooltip(
                "value:Q", format=ChartTheme.format_number("currency"), title="GDP per Worker"
            ),
            alt.Tooltip("year:Q", format="d", title="Year"),
        ],
    )
    .properties(
        width=500,
        height=500,
        title=ChartTheme.get_title_params(
            "GDP per Worker (Most Recent)", "Select countries to compare trends over time"
        ),
    )
)

brush = alt.selection_point(fields=["country_code"], name="brush")
chart = chart.add_params(brush).encode(
    opacity=alt.condition(brush, alt.value(ChartTheme.BAR_OPACITY), alt.value(0.3))
)

bar = chart

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
