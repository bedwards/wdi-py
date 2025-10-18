"""Tests for wdi.chart module."""

import pytest
import polars as pl
import altair as alt
from pathlib import Path
import tempfile
from wdi import chart


@pytest.fixture
def sample_df() -> pl.DataFrame:
    """Create sample DataFrame for testing."""
    return pl.DataFrame(
        {
            "country_code": ["USA", "CHN", "IND", "BRA", "ZAF"],
            "country_name": ["United States", "China", "India", "Brazil", "South Africa"],
            "x_value": [63000.0, 10500.0, 1900.0, 8700.0, 6000.0],
            "y_value": [78.5, 76.9, 69.7, 75.9, 64.1],
            "region": [
                "North America",
                "East Asia & Pacific",
                "South Asia",
                "Latin America & Caribbean",
                "Sub-Saharan Africa",
            ],
            "income_group": [
                "High income",
                "Upper middle income",
                "Lower middle income",
                "Upper middle income",
                "Upper middle income",
            ],
        }
    )


def test_scatter_with_filter_basic(sample_df: pl.DataFrame) -> None:
    """Test basic scatter plot creation."""
    chart_obj, brush = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        title="Test Scatter",
    )

    assert isinstance(chart_obj, alt.Chart)
    assert isinstance(brush, alt.Parameter)


def test_scatter_with_filter_with_color(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with color encoding."""
    chart_obj, brush = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        color="region",
        title="Test Scatter",
    )

    assert isinstance(chart_obj, alt.Chart)


def test_scatter_with_filter_log_scales(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with logarithmic scales."""
    chart_obj, brush = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        log_x=True,
        log_y=True,
    )

    assert isinstance(chart_obj, alt.Chart)


def test_bar_chart_filtered(sample_df: pl.DataFrame) -> None:
    """Test bar chart creation."""
    _, brush = chart.scatter_with_filter(df=sample_df, x="x_value", y="y_value")

    bar = chart.bar_chart_filtered(
        df=sample_df,
        x="region",
        y="count()",
        selection=brush,
    )

    assert isinstance(bar, alt.Chart)


def test_bar_chart_filtered_with_color(sample_df: pl.DataFrame) -> None:
    """Test bar chart with color encoding."""
    bar = chart.bar_chart_filtered(
        df=sample_df,
        x="income_group",
        y="count()",
        color="income_group",
    )

    assert isinstance(bar, alt.Chart)


def test_histogram_filtered(sample_df: pl.DataFrame) -> None:
    """Test histogram creation."""
    _, brush = chart.scatter_with_filter(df=sample_df, x="x_value", y="y_value")

    hist = chart.histogram_filtered(
        df=sample_df,
        column="x_value",
        bins=20,
        selection=brush,
    )

    assert isinstance(hist, alt.Chart)


def test_line_chart_filtered() -> None:
    """Test line chart creation."""
    ts_df = pl.DataFrame(
        {
            "country_code": ["USA", "USA", "CHN", "CHN"],
            "year": [2018, 2019, 2018, 2019],
            "value": [20000.0, 21000.0, 13000.0, 14000.0],
        }
    )

    line = chart.line_chart_filtered(
        df=ts_df,
        x="year",
        y="value",
        color="country_code",
    )

    assert isinstance(line, alt.Chart)


def test_save_linked_charts(sample_df: pl.DataFrame) -> None:
    """Test saving linked charts to HTML."""
    scatter, brush = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        color="region",
    )

    bar = chart.bar_chart_filtered(
        df=sample_df,
        x="region",
        y="count()",
        selection=brush,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_chart.html"
        chart.save_linked_charts(
            chart_left=scatter,
            chart_right=bar,
            filename=str(output_file),
        )

        assert output_file.exists()
        assert output_file.stat().st_size > 0


def test_save_linked_charts_with_title(sample_df: pl.DataFrame) -> None:
    """Test saving linked charts with overall title."""
    scatter, brush = chart.scatter_with_filter(df=sample_df, x="x_value", y="y_value")

    bar = chart.bar_chart_filtered(df=sample_df, x="region", y="count()", selection=brush)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_chart.html"
        chart.save_linked_charts(
            chart_left=scatter,
            chart_right=bar,
            filename=str(output_file),
            overall_title="Test Visualization",
        )

        assert output_file.exists()
