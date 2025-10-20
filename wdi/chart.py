"""Altair charting utilities for WDI data visualization with opinionated design system."""

import altair as alt
import polars as pl

# =============================================================================
# THEME CONFIGURATION - Centralized design system
# =============================================================================


class ChartTheme:
    """Opinionated design theme for WDI visualizations.

    Inspired by modern data journalism and expert designers, this theme
    provides a distinctive look while maintaining readability and accessibility.
    """

    # Color palette - Custom, sophisticated colors
    # Primary colors for categorical data (inspired by Tableau 10 but customized)
    COLORS = [
        "#1f77b4",  # Steel blue
        "#ff7f0e",  # Vibrant orange
        "#2ca02c",  # Forest green
        "#d62728",  # Crimson
        "#9467bd",  # Purple
        "#8c564b",  # Brown
        "#e377c2",  # Pink
        "#7f7f7f",  # Gray
        "#bcbd22",  # Olive
        "#17becf",  # Cyan
        "#393b79",  # Deep blue
        "#e7ba52",  # Gold
        "#5254a3",  # Dark purple
        "#8c6d31",  # Dark olive
        "#d95f0e",  # Dark orange
    ]

    # Accent colors
    ACCENT_PRIMARY = "#ff6b6b"  # Coral red
    ACCENT_SECONDARY = "#4ecdc4"  # Turquoise
    SELECTION_COLOR = "#2d3748"  # Dark slate
    DESELECTED_COLOR = "#e2e8f0"  # Light gray

    # Typography
    FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    TITLE_FONT_SIZE = 16
    TITLE_FONT_WEIGHT = 600
    SUBTITLE_FONT_SIZE = 13
    SUBTITLE_FONT_WEIGHT = 400
    SUBTITLE_COLOR = "#64748b"
    LABEL_FONT_SIZE = 11

    # Layout
    BACKGROUND_COLOR = "#ffffff"
    GRID_COLOR = "#f1f5f9"
    AXIS_COLOR = "#cbd5e1"
    PADDING = 20

    # Chart dimensions (default)
    WIDTH = 500
    HEIGHT = 400

    # Point/mark properties
    POINT_SIZE = 80
    POINT_OPACITY = 0.75
    POINT_OPACITY_SELECTED = 0.95
    LINE_STROKE_WIDTH = 2.5
    BAR_OPACITY = 0.9

    @classmethod
    def get_color_scale(cls, domain: list[str] | None = None) -> alt.Scale:
        """Get color scale with theme colors."""
        if domain is None:
            return alt.Scale(range=cls.COLORS)
        return alt.Scale(range=cls.COLORS, domain=domain)

    @classmethod
    def get_title_params(cls, title: str, subtitle: str | None = None) -> alt.TitleParams:
        """Create properly formatted title with optional subtitle.

        Follows notebook pattern: centered title and subtitle with proper spacing.
        """
        if subtitle is None:
            return alt.TitleParams(
                text=title,
                anchor="middle",
                align="center",
                fontSize=cls.TITLE_FONT_SIZE,
                fontWeight=cls.TITLE_FONT_WEIGHT,
                offset=15,
                orient="top",
            )

        return alt.TitleParams(
            text=title.capitalize(),
            subtitle=subtitle.capitalize(),
            anchor="middle",
            align="center",
            fontSize=cls.TITLE_FONT_SIZE,
            fontWeight=cls.TITLE_FONT_WEIGHT,
            subtitleFontSize=cls.SUBTITLE_FONT_SIZE,
            subtitleFontWeight=cls.SUBTITLE_FONT_WEIGHT,
            subtitleColor=cls.SUBTITLE_COLOR,
            subtitlePadding=8,
            offset=15,
            orient="top",
        )

    @classmethod
    def format_number(cls, value_type: str = "default") -> str:
        """Get number format string based on value type.

        Args:
            value_type: Type of value - 'currency', 'percent', 'large', 'decimal', 'default'
        """
        formats = {
            "currency": "$,.2s",  # $1.2M, $345.6k
            "percent": ".0%",
            "large": ",.2s",  # 1.2M, 345.6k
            "decimal": ".2f",  # 12.34
            "integer": "d",  # 1234
            "default": ",.0f",  # 1,234
        }
        return formats.get(value_type, formats["default"])

    @classmethod
    def format_axis_year(cls) -> str:
        """Format year axis - no decimals, no commas."""
        return "d"

    @classmethod
    def format_axis_percent(cls, decimals: int = 0) -> str:
        """Format percent axis with specified decimals."""
        return f".{decimals}f"


# =============================================================================
# SHARED PROPERTIES
# =============================================================================


def to_title(column: str) -> str:
    """Convert a column name to a human-readable title.

    Replaces underscores with spaces and capitalizes each word.

    Args:
        column (str): The column name to convert.

    Returns:
        str: A human-readable title.
    """
    if column == "income_group":
        return "Income"
    if column == "country_name":
        return "Country"
    return " ".join(column.split("_")).capitalize()


def legend(color: str) -> alt.Legend:
    """Create a legend configuration with theme-appropriate styling.

    Args:
        color: Color scale or color string to base the legend on.

    Returns:
        alt.Legend: Configured legend object.
    """
    return alt.Legend(
        titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
        labelFontSize=ChartTheme.LABEL_FONT_SIZE,
        title=to_title(color),
    )


def create_tooltip(
    x: str,
    y: str,
    color: str,
    x_axis_format: str,
    y_format: str,
    y_title: str,
    y2: str | None = None,
    y2_title: str | None = None,
) -> list[alt.Tooltip]:
    """Create a tooltip configuration for an Altair chart.

    Args:
        x: X-axis field for the tooltip.
        y: Y-axis field for the tooltip.
        color: Color field for the tooltip.
        x_axis_format: Format string for the x-axis values.
        y_format: Format string for the y-axis values.
        y_title: Title for the y-axis tooltip.
        y2: Optional second y-axis field for the tooltip.
        y2_title: Optional title for the second y-axis tooltip.

    Returns:
        alt.Tooltip: Configured tooltip object.
    """
    result = []

    if color:
        result.append(alt.Tooltip(color, title=to_title(color)))

    if y_title is None:
        y_title = to_title(y)

    y_title = " ".join(y_title.split(" ")[:2])

    if y2 is not None:
        if y2_title is None:
            y2_title = to_title(y2)
        y2_title = " ".join(y2_title.split(" ")[:2])

    result.extend(
        [
            alt.Tooltip("income_group:N", title="Income"),
            alt.Tooltip(x, format=x_axis_format, title=to_title(x)),
            alt.Tooltip(y, format=ChartTheme.format_number(y_format), title=y_title),
        ]
    )

    if y2 is not None:
        # result.append(alt.Tooltip(y2, format=ChartTheme.format_number(y2_format), title=y2_title))
        result.append(alt.Tooltip("y2_label:N", title=y2_title))

    return result


# =============================================================================
# CHART FUNCTIONS
# =============================================================================


def scatter_with_filter(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    tooltip: list[str] | None = None,
    title: str = "Scatter Plot",
    subtitle: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
    x_format: str = "default",
    y_format: str = "default",
    log_x: bool = False,
    log_y: bool = False,
    width: int = ChartTheme.WIDTH,
    height: int = ChartTheme.HEIGHT,
) -> tuple[alt.Chart, alt.Parameter]:
    """Create a scatter plot with interval selection.

    Args:
        df: Input DataFrame
        x: X-axis column name
        y: Y-axis column name
        color: Color encoding column
        tooltip: List of columns for tooltip
        title: Chart title
        subtitle: Chart subtitle
        x_title: X-axis title (defaults to column name)
        y_title: Y-axis title (defaults to column name)
        x_format: Format type for x-axis ('currency', 'percent', 'large', etc.)
        y_format: Format type for y-axis
        log_x: Use log scale for X-axis
        log_y: Use log scale for Y-axis
        width: Chart width
        height: Chart height

    Returns:
        Tuple of (chart, selection) where selection can be used to filter other charts
    """
    brush = alt.selection_interval(name="brush")

    x_scale = alt.Scale(type="log") if log_x else alt.Scale()
    y_scale = alt.Scale(type="log") if log_y else alt.Scale()

    base_tooltip = tooltip or [x, y]
    if color and color not in base_tooltip:
        base_tooltip.append(color)

    # Build tooltip with proper formatting
    tooltip_list = []
    for col in base_tooltip:
        if df[col].dtype in [pl.Float64, pl.Float32]:
            # Determine format based on column name hints
            fmt = ",.2f"
            if "gdp" in col.lower() or "income" in col.lower() or "capita" in col.lower():
                fmt = "$,.2s"
            elif "percent" in col.lower() or "rate" in col.lower():
                fmt = ".1f"
            tooltip_list.append(alt.Tooltip(col, format=fmt))
        else:
            tooltip_list.append(alt.Tooltip(col))

    chart = (
        alt.Chart(df)
        .mark_point(
            size=ChartTheme.POINT_SIZE,
            opacity=ChartTheme.POINT_OPACITY,
            filled=True,
        )
        .encode(
            x=alt.X(
                f"{x}:Q",
                title=x_title or x,
                scale=x_scale,
                axis=alt.Axis(
                    format=ChartTheme.format_number(x_format),
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                    gridColor=ChartTheme.GRID_COLOR,
                ),
            ),
            y=alt.Y(
                f"{y}:Q",
                title=y_title or y,
                scale=y_scale,
                axis=alt.Axis(
                    format=ChartTheme.format_number(y_format),
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                    gridColor=ChartTheme.GRID_COLOR,
                ),
            ),
            color=(
                alt.condition(
                    brush,
                    alt.Color(
                        f"{color}:N",
                        scale=ChartTheme.get_color_scale(),
                        legend=legend(color),
                    ),
                    alt.value(ChartTheme.DESELECTED_COLOR),
                )
                if color
                else alt.value(ChartTheme.COLORS[0])
            ),
            opacity=alt.condition(
                brush, alt.value(ChartTheme.POINT_OPACITY_SELECTED), alt.value(0.3)
            ),
            tooltip=tooltip_list,
        )
        .properties(
            width=width,
            height=height,
            title=ChartTheme.get_title_params(title, subtitle),
        )
        .add_params(brush)
    )

    return chart, brush


def bar_chart_filtered(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "Bar Chart",
    subtitle: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
    y_format: str = "default",
    width: int = 450,
    height: int = ChartTheme.HEIGHT,
    selection: alt.Parameter | None = None,
) -> alt.Chart:
    """Create a bar chart that responds to a selection filter.

    Args:
        df: Input DataFrame
        x: X-axis column name
        y: Y-axis column name (typically count or aggregation)
        color: Color encoding column
        title: Chart title
        subtitle: Chart subtitle
        x_title: X-axis title
        y_title: Y-axis title
        y_format: Format type for y-axis
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by

    Returns:
        Altair Chart object
    """
    chart = (
        alt.Chart(df)
        .mark_bar(
            opacity=ChartTheme.BAR_OPACITY,
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2,
        )
        .encode(
            x=alt.X(
                f"{x}:N",
                title=x_title or x,
                axis=alt.Axis(
                    labelAngle=-45 if len(df[x].unique()) > 5 else 0,
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                ),
            ),
            y=alt.Y(
                f"{y}:Q",
                title=y_title or y,
                axis=alt.Axis(
                    format=ChartTheme.format_number(y_format),
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                    gridColor=ChartTheme.GRID_COLOR,
                ),
            ),
            color=(
                alt.Color(
                    f"{color}:N",
                    scale=ChartTheme.get_color_scale(),
                    legend=legend(color),
                )
                if color
                else alt.value(ChartTheme.COLORS[0])
            ),
            tooltip=[
                alt.Tooltip(x),
                alt.Tooltip(y, format=ChartTheme.format_number(y_format)),
            ],
        )
        .properties(
            width=width,
            height=height,
            title=ChartTheme.get_title_params(title, subtitle),
        )
    )

    if selection:
        chart = chart.transform_filter(selection)

    return chart  # type: ignore[no-any-return]


def histogram_filtered(
    df: pl.DataFrame,
    column: str,
    bins: int = 30,
    title: str = "Histogram",
    subtitle: str | None = None,
    x_title: str | None = None,
    x_format: str = "default",
    width: int = 450,
    height: int = ChartTheme.HEIGHT,
    selection: alt.Parameter | None = None,
) -> alt.Chart:
    """Create a histogram that responds to a selection filter.

    Args:
        df: Input DataFrame
        column: Column to create histogram for
        bins: Number of bins
        title: Chart title
        subtitle: Chart subtitle
        x_title: X-axis title
        x_format: Format type for x-axis
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by

    Returns:
        Altair Chart object
    """
    chart = (
        alt.Chart(df)
        .mark_bar(
            opacity=ChartTheme.BAR_OPACITY,
            cornerRadiusTopLeft=2,
            cornerRadiusTopRight=2,
            color=ChartTheme.COLORS[0],
        )
        .encode(
            x=alt.X(
                f"{column}:Q",
                bin=alt.Bin(maxbins=bins),
                title=x_title or column,
                axis=alt.Axis(
                    format=ChartTheme.format_number(x_format),
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                ),
            ),
            y=alt.Y(
                "count()",
                title="Count",
                axis=alt.Axis(
                    labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                    titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                    gridColor=ChartTheme.GRID_COLOR,
                ),
            ),
            tooltip=[
                alt.Tooltip(f"{column}:Q", bin=True, format=ChartTheme.format_number(x_format)),
                alt.Tooltip("count()", title="Count"),
            ],
        )
        .properties(
            width=width,
            height=height,
            title=ChartTheme.get_title_params(title, subtitle),
        )
    )

    if selection:
        chart = chart.transform_filter(selection)

    return chart  # type: ignore[no-any-return]


class LineChartFiltered(alt.Chart):
    def mark_wdi(self):
        return self.mark_line(
            strokeWidth=ChartTheme.LINE_STROKE_WIDTH,
            point=alt.OverlayMarkDef(size=40, filled=True),
        )

    def encode_wdi(
        self,
        x: str,
        y: str,
        color: str | None = None,
        title: str = "Line Chart",
        subtitle: str | None = None,
        x_title: str | None = None,
        y_title: str | None = None,
        y_format: str = "default",
        width: int = 450,
        height: int = ChartTheme.HEIGHT,
        selection: alt.Parameter | None = None,
        y2: str | None = None,
        y2_title: str | None = None,
    ) -> alt.Chart:
        x_axis_format = (
            ChartTheme.format_axis_year()
            if "year" in x.lower()
            else ChartTheme.format_number("default")
        )

        chart = (
            self.transform_calculate(
                y2_label=f"datum.{y2} == null ? 'Not available' : toString(round(datum.{y2} * 100)) + '%'"
            )
            .encode(
                x=alt.X(
                    f"{x}:Q",
                    title=(x_title or x).capitalize(),
                    axis=alt.Axis(
                        format=x_axis_format,
                        labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                        titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                        gridColor=ChartTheme.GRID_COLOR,
                    ),
                ),
                y=alt.Y(
                    f"{y}:Q",
                    title=(y_title or y).capitalize(),
                    axis=alt.Axis(
                        format=ChartTheme.format_number(y_format),
                        labelFontSize=ChartTheme.LABEL_FONT_SIZE,
                        titleFontSize=ChartTheme.LABEL_FONT_SIZE + 1,
                        gridColor=ChartTheme.GRID_COLOR,
                    ),
                ),
                color=(
                    alt.Color(
                        f"{color}:N",
                        scale=ChartTheme.get_color_scale(),
                        legend=legend(color),
                    )
                    if color
                    else alt.value(ChartTheme.COLORS[0])
                ),
            )
            .properties(
                width=width,
                height=height,
                title=ChartTheme.get_title_params(title, subtitle),
            )
        )

        if y is not None and color is not None and y_title is not None:
            chart = chart.encode(
                tooltip=create_tooltip(x, y, color, x_axis_format, y_format, y_title, y2, y2_title)
            )

        if selection:
            chart = chart.transform_filter(selection)

        return chart  # type: ignore[no-any-return]


def line_chart_filtered(
    df: pl.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "Line Chart",
    subtitle: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
    y_format: str = "default",
    width: int = 450,
    height: int = ChartTheme.HEIGHT,
    selection: alt.Parameter | None = None,
) -> alt.Chart:
    """Create a line chart that responds to a selection filter.

    Args:
        df: Input DataFrame
        x: X-axis column name (typically year)
        y: Y-axis column name
        color: Color encoding column (typically country)
        title: Chart title
        subtitle: Chart subtitle
        x_title: X-axis title
        y_title: Y-axis title
        y_format: Format type for y-axis
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by

    Returns:
        Altair Chart object
    """
    return (
        LineChartFiltered(df)
        .mark_wdi()
        .encode_wdi(
            x,
            y,
            color,
            title,
            subtitle,
            x_title,
            y_title,
            y_format,
            width,
            height,
            selection,
        )
    )


def save_linked_charts(
    chart_left: alt.Chart,
    chart_right: alt.Chart,
    filename: str,
    overall_title: str | None = None,
    overall_subtitle: str | None = None,
) -> None:
    """Save two horizontally-aligned charts to an HTML file.

    Args:
        chart_left: Left chart (typically with selection)
        chart_right: Right chart (typically filtered by selection)
        filename: Output filename (should end in .html)
        overall_title: Optional overall title for the visualization
        overall_subtitle: Optional overall subtitle
    """
    combined = chart_left | chart_right

    # Apply background and other properties to the combined chart
    if overall_title:
        combined = combined.properties(
            title=ChartTheme.get_title_params(overall_title, overall_subtitle),
            padding=ChartTheme.PADDING,
            background=ChartTheme.BACKGROUND_COLOR,
        )
    else:
        combined = combined.properties(
            padding=ChartTheme.PADDING,
            background=ChartTheme.BACKGROUND_COLOR,
        )

    combined.save(filename)


def map_chart_filtered(
    df: pl.DataFrame,
    country_col: str = "country_code",
    value_col: str = "value",
    title: str = "World Map",
    subtitle: str | None = None,
    width: int = 600,
    height: int = 400,
    selection: alt.Parameter | None = None,
) -> alt.Chart:
    """Create a choropleth map that responds to a selection filter.

    Args:
        df: Input DataFrame with country codes (ISO 3166-1 alpha-3)
        country_col: Column containing country codes
        value_col: Column with values to visualize
        title: Chart title
        subtitle: Chart subtitle
        width: Chart width
        height: Chart height
        selection: Selection from another chart to filter by

    Returns:
        Altair Chart object
    """
    from vega_datasets import data as vega_data

    world_map = alt.topo_feature(vega_data.world_110m.url, "countries")

    chart = (
        alt.Chart(world_map)
        .mark_geoshape(
            stroke=ChartTheme.AXIS_COLOR,
            strokeWidth=0.5,
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(df, country_col, [value_col]),  # type: ignore[arg-type]
        )
        .encode(
            color=alt.Color(
                f"{value_col}:Q",
                scale=alt.Scale(scheme="blues"),
                legend=legend(value_col),
            ),
            tooltip=[
                alt.Tooltip(country_col),
                alt.Tooltip(value_col, format=ChartTheme.format_number("default")),
            ],
        )
        .properties(
            width=width,
            height=height,
            title=ChartTheme.get_title_params(title, subtitle),
        )
        .project("naturalEarth1")
    )

    if selection:
        chart = chart.transform_filter(selection)

    return chart  # type: ignore[no-any-return]
