"""Tests for wdi.chart module."""

import tempfile
from pathlib import Path

import altair as alt
import polars as pl
import pytest

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
            "year": [2020, 2020, 2020, 2020, 2020],
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


def test_chart_theme_colors() -> None:
    """Test that ChartTheme has expected colors."""
    assert len(chart.ChartTheme.COLORS) >= 10
    assert chart.ChartTheme.ACCENT_PRIMARY.startswith("#")
    assert chart.ChartTheme.SELECTION_COLOR.startswith("#")


def test_chart_theme_formats() -> None:
    """Test number formatting."""
    assert chart.ChartTheme.format_number("currency") == "$,.2s"
    assert chart.ChartTheme.format_number("percent") == ".0%"
    assert chart.ChartTheme.format_axis_year() == "d"
    assert "f" in chart.ChartTheme.format_axis_percent(1)


def test_chart_theme_title_params() -> None:
    """Test title parameter creation."""
    title_params = chart.ChartTheme.get_title_params("Test Title", "Test Subtitle")
    assert isinstance(title_params, alt.TitleParams)
    assert title_params.text == "Test title"
    assert title_params.subtitle == "Test subtitle"


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


def test_scatter_with_filter_with_subtitle(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with subtitle."""
    chart_obj, _ = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        title="Test Scatter",
        subtitle="Test Subtitle",
    )

    assert isinstance(chart_obj, alt.Chart)


def test_scatter_with_filter_with_color(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with color encoding."""
    chart_obj, _ = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        color="region",
        title="Test Scatter",
    )

    assert isinstance(chart_obj, alt.Chart)


def test_scatter_with_filter_log_scales(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with logarithmic scales."""
    chart_obj, _ = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        log_x=True,
        log_y=True,
    )

    assert isinstance(chart_obj, alt.Chart)


def test_scatter_with_filter_custom_formats(sample_df: pl.DataFrame) -> None:
    """Test scatter plot with custom formatting."""
    chart_obj, _ = chart.scatter_with_filter(
        df=sample_df,
        x="x_value",
        y="y_value",
        x_format="currency",
        y_format="decimal",
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


def test_bar_chart_with_subtitle(sample_df: pl.DataFrame) -> None:
    """Test bar chart with subtitle."""
    bar = chart.bar_chart_filtered(
        df=sample_df,
        x="income_group",
        y="count()",
        title="Test Bar",
        subtitle="Test Subtitle",
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


def test_histogram_with_custom_format(sample_df: pl.DataFrame) -> None:
    """Test histogram with custom formatting."""
    hist = chart.histogram_filtered(
        df=sample_df,
        column="x_value",
        bins=20,
        x_format="currency",
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


def test_line_chart_with_subtitle() -> None:
    """Test line chart with subtitle."""
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
        title="Test Line",
        subtitle="Test Subtitle",
    )

    assert isinstance(line, alt.Chart)


def test_line_chart_year_formatting() -> None:
    """Test that year column gets proper formatting."""
    ts_df = pl.DataFrame(
        {
            "year": [2018, 2019, 2020],
            "value": [100.0, 110.0, 120.0],
        }
    )

    line = chart.line_chart_filtered(
        df=ts_df,
        x="year",
        y="value",
        y_format="currency",
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


def test_save_linked_charts_with_subtitle(sample_df: pl.DataFrame) -> None:
    """Test saving linked charts with title and subtitle."""
    scatter, brush = chart.scatter_with_filter(df=sample_df, x="x_value", y="y_value")

    bar = chart.bar_chart_filtered(df=sample_df, x="region", y="count()", selection=brush)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_chart.html"
        chart.save_linked_charts(
            chart_left=scatter,
            chart_right=bar,
            filename=str(output_file),
            overall_title="Test Visualization",
            overall_subtitle="Test Subtitle",
        )

        assert output_file.exists()


def test_map_chart_filtered(sample_df: pl.DataFrame) -> None:
    """Test map chart creation."""
    map_chart = chart.map_chart_filtered(
        df=sample_df,
        country_col="country_code",
        value_col="x_value",
    )

    assert isinstance(map_chart, alt.Chart)


def test_map_chart_with_subtitle(sample_df: pl.DataFrame) -> None:
    """Test map chart with subtitle."""
    map_chart = chart.map_chart_filtered(
        df=sample_df,
        country_col="country_code",
        value_col="x_value",
        title="Test Map",
        subtitle="Test Subtitle",
    )

    assert isinstance(map_chart, alt.Chart)
