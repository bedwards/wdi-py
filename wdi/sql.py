"""SQL utilities for querying WDI PostgreSQL database."""

import os
from decimal import Decimal
from pathlib import Path

import polars as pl
import psycopg2
from psycopg2.extensions import connection as Connection


# Load environment variables from .env file if it exists
def _load_env() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


_load_env()


def _convert_decimals(rows: list[tuple]) -> list[tuple]:
    """Convert Decimal values to float for JSON serialization."""
    return [tuple(float(v) if isinstance(v, Decimal) else v for v in row) for row in rows]


def get_connection(
    host: str | None = None,
    port: int | None = None,
    database: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> Connection:
    """Create a connection to the WDI PostgreSQL database.

    Args:
        host: Database host (defaults to DB_HOST env var or 'localhost')
        port: Database port (defaults to DB_PORT env var or 5432)
        database: Database name (defaults to DB_NAME env var or 'db')
        user: Database user (defaults to DB_USER env var or 'postgres')
        password: Database password (defaults to DB_PASSWORD env var or None)

    Returns:
        PostgreSQL connection object
    """
    conn_params = {
        "host": host or os.getenv("DB_HOST", "localhost"),
        "port": port or os.getenv("DB_PORT", 5432),
        "database": database or os.getenv("DB_NAME", "db"),
        "user": user or os.getenv("DB_USER", "postgres"),
    }
    if password or os.getenv("DB_PASSWORD"):
        conn_params["password"] = password or os.getenv("DB_PASSWORD", "")

    return psycopg2.connect(None, None, None, **conn_params)


def query(sql: str, conn: Connection | None = None) -> pl.DataFrame:
    """Execute a SQL query and return results as a Polars DataFrame.

    Args:
        sql: SQL query string
        conn: Database connection (creates new one if None)

    Returns:
        Query results as Polars DataFrame
    """
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        df = pl.read_database(sql, conn)
        return df
    finally:
        if close_conn:
            conn.close()


def get_countries(
    region: str | None = None,
    income_group: str | None = None,
    conn: Connection | None = None,
) -> pl.DataFrame:
    """Get countries, optionally filtered by region or income group.

    Args:
        region: Filter by region name
        income_group: Filter by income group
        conn: Database connection

    Returns:
        DataFrame with country_code, country_name, region, income_group
    """
    sql = "SELECT country_code, country_name, region, income_group FROM wdi.countries WHERE 1=1"
    params: list[str | int] = []

    if region:
        sql += " AND region = %s"
        params.append(region)
    if income_group:
        sql += " AND income_group = %s"
        params.append(income_group)

    sql += " ORDER BY country_name"

    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        with conn.cursor() as cur:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description] if cur.description else []

            return pl.DataFrame(_convert_decimals(rows), schema=columns, orient="row")

    finally:
        if close_conn:
            conn.close()


def get_indicators(
    topic: str | None = None,
    search: str | None = None,
    conn: Connection | None = None,
) -> pl.DataFrame:
    """Get indicators, optionally filtered by topic or search term.

    Args:
        topic: Filter by topic
        search: Search in indicator_name (case-insensitive)
        conn: Database connection

    Returns:
        DataFrame with indicator_code, indicator_name, topic, etc.
    """
    sql = "SELECT * FROM wdi.indicators WHERE 1=1"
    params: list[str | int] = []

    if topic:
        sql += " AND topic = %s"
        params.append(topic)
    if search:
        sql += " AND LOWER(indicator_name) LIKE LOWER(%s)"
        params.append(f"%{search}%")

    sql += " ORDER BY indicator_name"

    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []

        return pl.DataFrame(_convert_decimals(rows), schema=columns, orient="row")

    finally:
        if close_conn:
            conn.close()


def get_values(
    indicator_code: str,
    year: int | None = None,
    country_code: str | None = None,
    start_year: int | None = None,
    end_year: int | None = None,
    conn: Connection | None = None,
) -> pl.DataFrame:
    """Get indicator values with flexible filtering.

    Args:
        indicator_code: Indicator code to retrieve
        year: Specific year (overrides start_year/end_year)
        country_code: Filter by country code
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        conn: Database connection

    Returns:
        DataFrame with country_code, country_name, indicator_code,
        indicator_name, year, value
    """
    sql = "SELECT * FROM wdi.values WHERE indicator_code = %s"
    params = [indicator_code]

    if year is not None:
        sql += " AND year = %s"
        params.append(str(year))
    else:
        if start_year is not None:
            sql += " AND year >= %s"
            params.append(str(start_year))
        if end_year is not None:
            sql += " AND year <= %s"
            params.append(str(end_year))

    if country_code:
        sql += " AND country_code = %s"
        params.append(country_code)

    sql += " ORDER BY country_name, year"

    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []

        return pl.DataFrame(_convert_decimals(rows), schema=columns, orient="row")

    finally:
        if close_conn:
            conn.close()
