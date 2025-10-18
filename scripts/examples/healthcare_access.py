"""Healthcare Spending and Access.

Explore how healthcare expenditure relates to health outcomes.
Select countries on the scatter to see how their health spending
has evolved over time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi
import polars as pl

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get health expenditure and infant mortality for 2019
df = wdi.df.get_indicator_pairs(
    indicator_x="SH.XPD.CHEX.PC.CD",  # Current health expenditure per capita
    indicator_y="SP.DYN.IMRT.IN",     # Infant mortality rate (per 1,000 live births)
    year=2019,
    include_region=True,
    include_income_group=True,
)

# Remove nulls
df = df.filter(
    df["x_value"].is_not_null() & df["y_value"].is_not_null()
)

print(f"Analyzing {len(df)} countries with health spending and mortality data for 2019")

# Create scatter plot
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="region",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title="Health Expenditure vs Infant Mortality (2019)",
    x_title="Health Expenditure per Capita (US$, log scale)",
    y_title="Infant Mortality Rate (per 1,000 births, log scale)",
    log_x=True,
    log_y=True,
    width=500,
    height=500,
)

# Get time series for health expenditure of all countries
# Then filter to selected countries
ts_df = wdi.df.get_time_series(
    indicator_code="SH.XPD.CHEX.PC.CD",
    country_codes=df["country_code"].to_list(),
    start_year=2000,
    end_year=2019,
)

# Create line chart for selected countries
line = wdi.chart.line_chart_filtered(
    df=ts_df,
    x="year",
    y="value",
    color="country_code",
    title="Health Spending Over Time (Selected Countries)",
    x_title="Year",
    y_title="Health Expenditure per Capita (US$)",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "healthcare_access.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=line,
    filename=str(output_file),
    overall_title="Healthcare Investment and Outcomes: Select countries to see spending trends",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Do diminishing returns appear in health spending?")
print("- Which countries achieve low mortality with modest spending?")
print("- How has health spending grown over the past two decades?")
