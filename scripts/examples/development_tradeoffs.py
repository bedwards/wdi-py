"""Development and Environmental Tradeoffs.

Examine the relationship between economic growth (GDP per capita) and
environmental impact (CO2 emissions per capita). Select countries on the
scatter plot to see their emission distribution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import wdi

output_dir = Path("data/output")
output_dir.mkdir(parents=True, exist_ok=True)

year = 2018

co2_indicators = wdi.sql.get_indicators(search="CO2")
print(co2_indicators[["indicator_code", "indicator_name"]])

test_codes = ["EN.ATM.CO2E.PC", "EN.CO2.EMIS.PC", "EN.GHG.CO2.PC.CE.AR5"]
for code in test_codes:
    test_df = wdi.sql.get_values(indicator_code=code, year=2018)
    print(f"{code}: {len(test_df)} rows")

# Get GDP per capita and CO2 emissions for `year`
df = wdi.df.get_indicator_pairs(
    indicator_x="NY.GDP.PCAP.CD",  # GDP per capita (current US$)
    # indicator_y="EN.ATM.CO2E.PC",  # CO2 emissions (metric tons per capita)
    # indicator_y="EN.ATM.CO2E.KT",  # CO2 emissions (kt)
    indicator_y="EN.CO2.EMIS.PC",
    year=year,
    include_region=True,
    include_income_group=True,
)
df = df.filter(df["x_value"].is_not_null() & df["y_value"].is_not_null())

print(f"Analyzing {len(df)} countries with GDP and CO2 data for {year}")
print(f"Data shape: {df.shape}")
print("Looking for indicator_x: NY.GDP.PCAP.CD")
print("Looking for indicator_y: EN.ATM.CO2E.PC")
print(f"For year: {year}")

# Try getting them separately to see which one fails:
df_x = wdi.sql.get_values(indicator_code="NY.GDP.PCAP.CD", year=year)
print(f"X indicator has {len(df_x)} rows")
df_y = wdi.sql.get_values(indicator_code="EN.ATM.CO2E.PC", year=year)
print(f"Y indicator has {len(df_y)} rows")

if len(df) == 0:
    print("\n❌ No data found! Trying alternative indicators...")

    # Try different years
    for test_year in [2018, 2017, 2016, 2015]:
        test_df = wdi.df.get_indicator_pairs(
            indicator_x="NY.GDP.PCAP.CD",
            indicator_y="EN.ATM.CO2E.PC",
            year=test_year,
            include_region=True,
            include_income_group=True,
        )
        test_df = test_df.filter(
            test_df["x_value"].is_not_null() & test_df["y_value"].is_not_null()
        )
        if len(test_df) > 0:
            print(f"✓ Found {len(test_df)} countries with data for {test_year}")
            df = test_df
            year = test_year
            break

# Create scatter plot with logarithmic x-axis
scatter, brush = wdi.chart.scatter_with_filter(
    df=df,
    x="x_value",
    y="y_value",
    color="income_group",
    tooltip=["country_name", "x_value", "y_value", "region", "income_group"],
    title=f"Economic Development vs Carbon Emissions ({year})",
    subtitle="The environmental cost of prosperity",
    x_title="GDP per Capita (US$, log scale)",
    y_title="CO2 Emissions per Capita (metric tons)",
    x_format="currency",
    y_format="decimal",
    log_x=True,
    width=500,
    height=500,
)

# Create histogram of CO2 emissions for selected countries
histogram = wdi.chart.histogram_filtered(
    df=df,
    column="y_value",
    bins=30,
    title="Distribution of CO2 Emissions",
    subtitle="Selected countries",
    x_title="CO2 per Capita (metric tons)",
    x_format="decimal",
    width=450,
    height=500,
    selection=brush,
)

# Save linked charts
output_file = output_dir / "development_tradeoffs.html"
wdi.chart.save_linked_charts(
    chart_left=scatter,
    chart_right=histogram,
    filename=str(output_file),
    overall_title="The Carbon Cost of Development",
    overall_subtitle="Select countries to examine emission patterns",
)

print(f"\n✓ Saved: {output_file}")
print("\nQuestions to explore:")
print("- Is there a decoupling of wealth and emissions in high-income countries?")
print("- Which low-GDP countries have disproportionately high emissions?")
print("- What does the distribution tell us about global inequality in emissions?")
