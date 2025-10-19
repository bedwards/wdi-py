"""Inequality and Geographic Distribution.

Explore how income inequality (Gini coefficient) varies across regions.
Select countries on the left to see their regional distribution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import altair as alt

import wdi
from wdi.chart import ChartTheme

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get Gini coefficient data with regional information
df = wdi.df.get_indicator_data(
    indicator_code="SI.POV.GINI",  # Gini index
    include_region=True,
    include_income_group=True,
)

# Filter to most recent year per country
df = wdi.df.filter_latest_year(df)

# Remove null values
df = df.filter(df["value"].is_not_null())

print(f"Analyzing {len(df)} countries with Gini coefficient data")
print(f"Years covered: {df['year'].min()} - {df['year'].max()}")

brush = alt.selection_point(fields=["country_code"], name="brush")

# Create horizontal scatter plot
scatter = (
    alt.Chart(df)
    .mark_point(
        size=ChartTheme.POINT_SIZE,
        opacity=ChartTheme.POINT_OPACITY,
        filled=True,
    )
    .encode(
        x=alt.X(
            "value:Q",
            title="Gini Coefficient",
            axis=alt.Axis(
                format=ChartTheme.format_number("decimal"),
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
                labelFontSize=9,  # Smaller for many countries
                titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
            ),
        ),
        color=alt.condition(
            brush,
            alt.Color(
                "region:N",
                scale=ChartTheme.get_color_scale(),
                legend=alt.Legend(
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                ),
            ),
            alt.value(ChartTheme.DESELECTED_COLOR),
        ),
        opacity=alt.condition(brush, alt.value(ChartTheme.POINT_OPACITY_SELECTED), alt.value(0.3)),
        tooltip=[
            alt.Tooltip("country_name:N"),
            alt.Tooltip("value:Q", format=".2f", title="Gini Coefficient"),
            alt.Tooltip("year:Q", format="d"),
            alt.Tooltip("region:N"),
            alt.Tooltip("income_group:N"),
        ],
    )
    .properties(
        width=500,
        height=600,
        title=ChartTheme.get_title_params(
            "Income Inequality by Country", "Gini Coefficient (higher = more unequal)"
        ),
    )
)

scatter = scatter.add_params(brush)

# Create bar chart showing regional distribution
bar = wdi.chart.bar_chart_filtered(
    df=df,
    x="region",
    y="count()",
    color="region",
    title="Regional Distribution",
    subtitle="Number of selected countries by region",
    x_title="Region",
    y_title="Number of Countries",
    y_format="integer",
    width=450,
    height=600,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "inequality_geography.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=bar,
    filename=str(output_file),
    overall_title="Global Income Inequality: Select countries to explore regional patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nInsights to explore:")
print("- Which regions have the highest concentration of unequal countries?")
print("- Are high-inequality countries clustered geographically?")
print("- How does inequality vary within regions?")
