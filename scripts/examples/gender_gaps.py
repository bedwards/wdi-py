"""Gender Gaps in Economic Participation.

Explore the gender gap in labor force participation across countries.
Select countries to see how regional patterns emerge and how gaps have
changed over time.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi
import polars as pl

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Get labor force participation rates for both genders
male_df = wdi.sql.get_values(
    indicator_code="SL.TLF.CACT.MA.ZS",  # Male labor force participation
    year=2021,
)

female_df = wdi.sql.get_values(
    indicator_code="SL.TLF.CACT.FE.ZS",  # Female labor force participation
    year=2021,
)

# Join and calculate gap
df = male_df.join(
    female_df.select(["country_code", "value"]),
    on="country_code",
    how="inner",
    suffix="_female",
).rename({"value": "male_rate", "value_female": "female_rate"})

# Calculate gender gap (male rate - female rate)
df = df.with_columns((pl.col("male_rate") - pl.col("female_rate")).alias("gender_gap"))

# Add region and income group
countries = wdi.sql.get_countries()
df = df.join(
    countries.select(["country_code", "region", "income_group"]),
    on="country_code",
    how="left",
)

# Remove nulls
df = df.filter(df["gender_gap"].is_not_null() & df["region"].is_not_null())

print(f"Analyzing {len(df)} countries with labor force participation data for 2021")
print(f"Average gender gap: {df['gender_gap'].mean():.1f} percentage points")

# Create scatter plot: female rate vs male rate
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="female_rate",
    y="male_rate",
    color="region",
    tooltip=["country_name", "female_rate", "male_rate", "gender_gap", "region"],
    title="Gender Gap in Labor Force Participation (2021)",
    x_title="Female Labor Force Participation Rate (%)",
    y_title="Male Labor Force Participation Rate (%)",
    width=500,
    height=500,
)

# Create histogram of gender gaps for selected countries
histogram = wdi.chart.histogram_filtered(
    df=df,
    column="gender_gap",
    bins=25,
    title="Distribution of Gender Gap (Selected Countries)",
    x_title="Gender Gap (percentage points)",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "gender_gaps.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=histogram,
    filename=str(output_file),
    overall_title="Economic Gender Inequality: Select countries to explore participation gaps",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Which countries have the smallest gender gaps?")
print("- Is there a correlation between male and female participation rates?")
print("- How do gender gaps cluster by region?")
print("\nNote: Points closer to the diagonal line indicate smaller gender gaps")
