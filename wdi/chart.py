"""Altair charting utilities for WDI data visualization."""

from typing import Optional
import altair as alt
import polars as pl


def scatter_with_filter(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    tooltip: Optional[list[str]] = None,
    title: str = "Scatter Plot",
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    log_x: bool = False,
    log_y: bool = False,
    width: int = 400,
    height: int = 400,
) -> tuple[alt.Chart, alt.Parameter]:
    """Create a scatter plot with interval selection.
    
    Args:
        df: Input DataFrame
        x: X-axis column name
        y: Y-axis column name
        color: Color encoding column
        tooltip: List of columns for tooltip
        title: Chart title
        x_title: X-axis title (defaults to column name)
        y_title: Y-axis title (defaults to column name)
        log_x: Use log scale for X-axis
        log_y: Use log scale for Y-axis
        width: Chart width
        height: Chart height
    
    Returns:
        Tuple of (chart, selection) where selection can be used to filter other charts
    """
    brush = alt.selection_interval()
    
    x_scale = alt.Scale(type="log") if log_x else alt.Scale()
    y_scale = alt.Scale(type="log") if log_y else alt.Scale()
    
    base_tooltip = tooltip or [x, y]
    if color and color not in base_tooltip:
        base_tooltip.append(color)
    
    chart = (
        alt.Chart(df)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X(f"{x}:Q", title=x_title or x, scale=x_scale),
            y=alt.Y(f"{y}:Q", title=y_title or y, scale=y_scale),
            color=(
                alt.condition(brush, f"{color}:N", alt.value("lightgray"))
                if color
                else alt.value("steelblue")
            ),
            tooltip=[alt.Tooltip(col, format=".2f") if df[col].dtype in [pl.Float64, pl.Float32] else alt.Tooltip(col) 
                     for col in base_tooltip],
        )
        .properties(width=width, height=height, title=title)
        .add_params(brush)
    )
    
    return chart, brush


def bar_chart_filtered(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    title: str = "Bar Chart",
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    width: int = 400,
    height: int = 400,
    selection: Optional[alt.selection_interval] = None,
) -> alt.Chart:
    """Create a bar chart that responds to a selection filter.
    
    Args:
        df: Input DataFrame
        x: X-axis column name
        y: Y-axis column name (typically count or aggregation)
        color: Color encoding column
        title: Chart title
        x_title: X-axis title
        y_title: Y-axis title
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by
    
    Returns:
        Altair Chart object
    """
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{x}:N", title=x_title or x),
            y=alt.Y(f"{y}:Q", title=y_title or y),
            color=f"{color}:N" if color else alt.value("steelblue"),
            tooltip=[x, y],
        )
        .properties(width=width, height=height, title=title)
    )
    
    if selection:
        chart = chart.transform_filter(selection)
    
    return chart


def histogram_filtered(
    df: pl.DataFrame,
    column: str,
    bins: int = 30,
    title: str = "Histogram",
    x_title: Optional[str] = None,
    width: int = 400,
    height: int = 400,
    selection: Optional[alt.selection_interval] = None,
) -> alt.Chart:
    """Create a histogram that responds to a selection filter.
    
    Args:
        df: Input DataFrame
        column: Column to create histogram for
        bins: Number of bins
        title: Chart title
        x_title: X-axis title
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by
    
    Returns:
        Altair Chart object
    """
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{column}:Q", bin=alt.Bin(maxbins=bins), title=x_title or column),
            y=alt.Y("count()", title="Count"),
            tooltip=["count()"],
        )
        .properties(width=width, height=height, title=title)
    )
    
    if selection:
        chart = chart.transform_filter(selection)
    
    return chart


def line_chart_filtered(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    title: str = "Line Chart",
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    width: int = 400,
    height: int = 400,
    selection: Optional[alt.selection_interval] = None,
) -> alt.Chart:
    """Create a line chart that responds to a selection filter.
    
    Args:
        df: Input DataFrame
        x: X-axis column name (typically year)
        y: Y-axis column name
        color: Color encoding column (typically country)
        title: Chart title
        x_title: X-axis title
        y_title: Y-axis title
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by
    
    Returns:
        Altair Chart object
    """
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(f"{x}:Q", title=x_title or x),
            y=alt.Y(f"{y}:Q", title=y_title or y),
            color=f"{color}:N" if color else alt.value("steelblue"),
            tooltip=[x, y] + ([color] if color else []),
        )
        .properties(width=width, height=height, title=title)
    )
    
    if selection:
        chart = chart.transform_filter(selection)
    
    return chart


def save_linked_charts(
    chart_left: alt.Chart,
    chart_right: alt.Chart,
    filename: str,
    overall_title: Optional[str] = None,
) -> None:
    """Save two horizontally-aligned charts to an HTML file.
    
    Args:
        chart_left: Left chart (typically with selection)
        chart_right: Right chart (typically filtered by selection)
        filename: Output filename (should end in .html)
        overall_title: Optional overall title for the visualization
    """
    combined = (chart_left | chart_right)
    
    if overall_title:
        combined = combined.properties(title=overall_title)
    
    combined.save(filename)


def map_chart_filtered(
    df: pl.DataFrame,
    country_col: str = "country_code",
    value_col: str = "value",
    title: str = "World Map",
    width: int = 600,
    height: int = 400,
    selection: Optional[alt.selection_interval] = None,
) -> alt.Chart:
    """Create a choropleth map that responds to a selection filter.
    
    Args:
        df: Input DataFrame with country codes (ISO 3166-1 alpha-3)
        country_col: Column containing country codes
        value_col: Column with values to visualize
        title: Chart title
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by
    
    Returns:
        Altair Chart object
    """
    # Load world map data
    world_map = alt.topo_feature(alt.datasets.world_110m.url, "countries")
    
    # Convert 3-letter codes to numeric IDs (this is a simplification)
    # In practice, you'd need a proper mapping
    chart = (
        alt.Chart(world_map)
        .mark_geoshape()
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(df, country_col, [value_col]),
        )
        .encode(
            color=alt.Color(f"{value_col}:Q", scale=alt.Scale(scheme="viridis")),
            tooltip=[country_col, value_col],
        )
        .properties(width=width, height=height, title=title)
        .project("naturalEarth1")
    )
    
    if selection:
        chart = chart.transform_filter(selection)
    
    return chart
