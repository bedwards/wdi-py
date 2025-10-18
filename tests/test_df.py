"""Tests for wdi.df module."""

from unittest.mock import patch

import polars as pl
import pytest

from wdi import df


@pytest.fixture
def sample_values_df() -> pl.DataFrame:
    """Create sample values DataFrame."""
    return pl.DataFrame(
        {
            "id": [1, 2, 3],
            "country_code": ["USA", "CHN", "IND"],
            "country_name": ["United States", "China", "India"],
            "indicator_code": ["NY.GDP.MKTP.CD"] * 3,
            "indicator_name": ["GDP (current US$)"] * 3,
            "year": [2020, 2020, 2020],
            "value": [21000.0, 14700.0, 2700.0],
        }
    )


@pytest.fixture
def sample_countries_df() -> pl.DataFrame:
    """Create sample countries DataFrame."""
    return pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND"],
            "country_name": ["United States", "China", "India"],
            "region": ["North America", "East Asia & Pacific", "South Asia"],
            "income_group": ["High income", "Upper middle income", "Lower middle income"],
        }
    )


def test_get_indicator_data_basic(sample_values_df: pl.DataFrame) -> None:
    """Test get_indicator_data without metadata."""
    with patch("wdi.sql.get_values", return_value=sample_values_df):
        result = df.get_indicator_data("NY.GDP.MKTP.CD", year=2020)
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 3
        assert "region" not in result.columns


def test_get_indicator_data_with_region(
    sample_values_df: pl.DataFrame, sample_countries_df: pl.DataFrame
) -> None:
    """Test get_indicator_data with region metadata."""
    with (
        patch("wdi.sql.get_values", return_value=sample_values_df),
        patch("wdi.sql.get_countries", return_value=sample_countries_df),
    ):
        result = df.get_indicator_data("NY.GDP.MKTP.CD", year=2020, include_region=True)
        assert "region" in result.columns
        assert "income_group" not in result.columns


def test_get_indicator_data_with_income_group(
    sample_values_df: pl.DataFrame, sample_countries_df: pl.DataFrame
) -> None:
    """Test get_indicator_data with income group metadata."""
    with (
        patch("wdi.sql.get_values", return_value=sample_values_df),
        patch("wdi.sql.get_countries", return_value=sample_countries_df),
    ):
        result = df.get_indicator_data("NY.GDP.MKTP.CD", year=2020, include_income_group=True)
        assert "income_group" in result.columns
        assert "region" not in result.columns


def test_get_indicator_pairs() -> None:
    """Test get_indicator_pairs for scatter plots."""
    df_x = pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND"],
            "country_name": ["United States", "China", "India"],
            "indicator_code": ["NY.GDP.PCAP.CD"] * 3,
            "indicator_name": ["GDP per capita"] * 3,
            "year": [2020] * 3,
            "value": [63000.0, 10500.0, 1900.0],
        }
    )

    df_y = pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND"],
            "value": [78.5, 76.9, 69.7],
        }
    )

    countries = pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND"],
            "region": ["North America", "East Asia & Pacific", "South Asia"],
        }
    )

    with (
        patch("wdi.sql.get_values", side_effect=[df_x, df_y]),
        patch("wdi.sql.get_countries", return_value=countries),
    ):
        result = df.get_indicator_pairs(
            "NY.GDP.PCAP.CD", "SP.DYN.LE00.IN", 2020, include_region=True
        )

        assert "x_value" in result.columns
        assert "y_value" in result.columns
        assert "region" in result.columns
        assert len(result) == 3


def test_get_time_series() -> None:
    """Test get_time_series for multiple countries."""
    mock_df = pl.DataFrame(
        {
            "country_code": ["USA", "USA", "CHN", "CHN", "IND", "IND"],
            "country_name": ["United States"] * 2 + ["China"] * 2 + ["India"] * 2,
            "year": [2019, 2020, 2019, 2020, 2019, 2020],
            "value": [21000.0, 21500.0, 14200.0, 14700.0, 2600.0, 2700.0],
        }
    )

    with patch("wdi.sql.get_values", return_value=mock_df):
        result = df.get_time_series(
            "NY.GDP.MKTP.CD", ["USA", "CHN"], start_year=2019, end_year=2020
        )

        assert len(result) == 4
        assert set(result["country_code"].unique()) == {"USA", "CHN"}


def test_pivot_wide() -> None:
    """Test pivot_wide transformation."""
    long_df = pl.DataFrame(
        {
            "country_code": ["USA", "USA", "CHN", "CHN"],
            "year": [2019, 2020, 2019, 2020],
            "value": [21000.0, 21500.0, 14200.0, 14700.0],
        }
    )

    result = df.pivot_wide(long_df)

    assert "2019" in result.columns
    assert "2020" in result.columns
    assert len(result) == 2


def test_calculate_growth_rate() -> None:
    """Test calculate_growth_rate."""
    input_df = pl.DataFrame(
        {
            "country_code": ["USA", "USA", "USA"],
            "year": [2018, 2019, 2020],
            "value": [20000.0, 21000.0, 21500.0],
        }
    )

    result = df.calculate_growth_rate(input_df)

    assert "growth_rate" in result.columns
    # First row should be null
    assert result["growth_rate"][0] is None
    # Second row: (21000 - 20000) / 20000 * 100 = 5.0
    assert abs(result["growth_rate"][1] - 5.0) < 0.01


def test_rank_countries() -> None:
    """Test rank_countries."""
    input_df = pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND"],
            "value": [21000.0, 14700.0, 2700.0],
        }
    )

    result = df.rank_countries(input_df, descending=True)

    assert "rank" in result.columns
    # USA should be rank 1 (highest)
    usa_rank = result.filter(pl.col("country_code") == "USA")["rank"][0]
    assert usa_rank == 1


def test_aggregate_by_region() -> None:
    """Test aggregate_by_region."""
    input_df = pl.DataFrame(
        {
            "region": ["North America", "North America", "East Asia"],
            "value": [21000.0, 1700.0, 14700.0],
        }
    )

    result = df.aggregate_by_region(input_df, agg_func="mean")

    assert "value_mean" in result.columns
    assert len(result) == 2


def test_aggregate_by_region_no_region_column() -> None:
    """Test aggregate_by_region raises error without region column."""
    input_df = pl.DataFrame(
        {
            "country_code": ["USA", "CHN"],
            "value": [21000.0, 14700.0],
        }
    )

    with pytest.raises(ValueError, match="must have 'region' column"):
        df.aggregate_by_region(input_df)


def test_filter_latest_year() -> None:
    """Test filter_latest_year."""
    input_df = pl.DataFrame(
        {
            "country_code": ["USA", "USA", "USA", "CHN", "CHN"],
            "year": [2018, 2019, 2020, 2019, 2020],
            "value": [20000.0, 21000.0, 21500.0, 14200.0, 14700.0],
        }
    )

    result = df.filter_latest_year(input_df)

    assert len(result) == 2
    assert set(result["year"].unique()) == {2020}
