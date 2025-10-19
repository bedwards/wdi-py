"""Polars DataFrame utilities for WDI data analysis."""

import polars as pl

from . import sql


def get_indicator_data(
    indicator_code: str,
    year: int | None = None,
    start_year: int | None = None,
    end_year: int | None = None,
    include_region: bool = False,
    include_income_group: bool = False,
) -> pl.DataFrame:
    """Get indicator data with optional country metadata.

    Args:
        indicator_code: Indicator code to retrieve
        year: Specific year
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        include_region: Join region information
        include_income_group: Join income group information

    Returns:
        DataFrame with indicator values and optional metadata
    """
    df = sql.get_values(
        indicator_code=indicator_code,
        year=year,
        start_year=start_year,
        end_year=end_year,
    )

    if include_region or include_income_group:
        countries = sql.get_countries()
        cols_to_join = ["country_code"]
        if include_region:
            cols_to_join.append("region")
        if include_income_group:
            cols_to_join.append("income_group")

        df = df.join(
            countries.select(cols_to_join),
            on="country_code",
            how="left",
        )

    return df


def get_indicator_pairs(
    indicator_x: str,
    indicator_y: str,
    year: int,
    include_region: bool = False,
    include_income_group: bool = False,
) -> pl.DataFrame:
    """Get paired indicator values for scatter plots.

    Args:
        indicator_x: X-axis indicator code
        indicator_y: Y-axis indicator code
        year: Year to retrieve
        include_region: Include region information
        include_income_group: Include income group information

    Returns:
        DataFrame with x_value, y_value, and country metadata
    """
    # Get both indicators
    df_x = sql.get_values(indicator_code=indicator_x, year=year)
    df_y = sql.get_values(indicator_code=indicator_y, year=year)

    # Join on country_code
    df = df_x.join(
        df_y.select(["country_code", "value"]),
        on="country_code",
        how="inner",
        suffix="_y",
    ).rename({"value": "x_value", "value_y": "y_value"})

    # Add metadata if requested
    if include_region or include_income_group:
        countries = sql.get_countries()
        cols_to_join = ["country_code"]
        if include_region:
            cols_to_join.append("region")
        if include_income_group:
            cols_to_join.append("income_group")

        df = df.join(
            countries.select(cols_to_join),
            on="country_code",
            how="left",
        )

    return df


def get_time_series(
    indicator_code: str,
    country_codes: list[str],
    start_year: int | None = None,
    end_year: int | None = None,
) -> pl.DataFrame:
    """Get time series data for multiple countries.

    Args:
        indicator_code: Indicator code to retrieve
        country_codes: List of country codes
        start_year: Start year (inclusive)
        end_year: End year (inclusive)

    Returns:
        DataFrame with year, value for each country
    """
    df = sql.get_values(
        indicator_code=indicator_code,
        start_year=start_year,
        end_year=end_year,
    )

    return df.filter(pl.col("country_code").is_in(country_codes))


def pivot_wide(
    df: pl.DataFrame,
    index_col: str = "country_code",
    year_col: str = "year",
    value_col: str = "value",
) -> pl.DataFrame:
    """Pivot long-format data to wide format with years as columns.

    Args:
        df: Input DataFrame in long format
        index_col: Column to use as index (typically country_code)
        year_col: Column containing years
        value_col: Column containing values

    Returns:
        Wide-format DataFrame with years as columns
    """
    return df.pivot(
        index=index_col,
        on=year_col,
        values=value_col,
    )

def calculate_growth_rate(
    df: pl.DataFrame,
    value_col: str = "value",
    periods: int = 1,
) -> pl.DataFrame:
    """Calculate period-over-period growth rates.

    Args:
        df: Input DataFrame (must be sorted by year within groups)
        value_col: Column containing values
        periods: Number of periods for growth calculation

    Returns:
        DataFrame with growth_rate column added
    """
    return df.with_columns(
        (
            (pl.col(value_col) - pl.col(value_col).shift(periods))
            / pl.col(value_col).shift(periods)
            * 100
        ).alias("growth_rate")
    )


def rank_countries(
    df: pl.DataFrame,
    value_col: str = "value",
    descending: bool = True,
) -> pl.DataFrame:
    """Rank countries by indicator value.

    Args:
        df: Input DataFrame
        value_col: Column to rank by
        descending: True for highest first, False for lowest first

    Returns:
        DataFrame with rank column added
    """
    return df.with_columns(
        pl.col(value_col).rank(method="ordinal", descending=descending).alias("rank")
    )


def aggregate_by_region(
    df: pl.DataFrame,
    value_col: str = "value",
    agg_func: str = "mean",
) -> pl.DataFrame:
    """Aggregate indicator values by region.

    Args:
        df: Input DataFrame (must have 'region' column)
        value_col: Column to aggregate
        agg_func: Aggregation function ('mean', 'sum', 'median', etc.)

    Returns:
        DataFrame aggregated by region
    """
    if "region" not in df.columns:
        raise ValueError("DataFrame must have 'region' column")

    agg_expr = getattr(pl.col(value_col), agg_func)()

    return df.group_by("region").agg(agg_expr.alias(f"{value_col}_{agg_func}"))


def filter_latest_year(df: pl.DataFrame) -> pl.DataFrame:
    """Filter to most recent year with data for each country.

    Args:
        df: Input DataFrame with year column

    Returns:
        DataFrame filtered to latest year per country
    """
    return df.filter(pl.col("year") == pl.col("year").max().over("country_code"))
