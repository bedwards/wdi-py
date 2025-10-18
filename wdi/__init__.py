"""WDI: World Development Indicators data analysis toolkit.

This package provides utilities for working with World Bank Development Indicators
data stored in PostgreSQL, with Polars for data manipulation and Altair for
interactive visualizations.
"""

__version__ = "0.1.0"

from . import chart, df, sql

__all__ = ["sql", "df", "chart"]
