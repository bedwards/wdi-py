"""SQL utilities for querying WDI PostgreSQL database."""

import polars as pl
import psycopg2
from psycopg2.extensions import connection as Connection


def get_connection(
    host: str = "localhost",
    port: int = 5432,
    database: str = "db",
    user: str = "postgres",
    password: str | None = None,
) -> Connection:
    """Create a connection to the WDI PostgreSQL database.

    Args:
        host: Database host
        port: Database port
        database: Database name
        user: Database user
        password: Database password (None uses trust authentication)

    Returns:
        PostgreSQL connection object
    """
    conn_params = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
    }
    if password:
        conn_params["password"] = password

    return psycopg2.connect(**conn_params)


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
    params = []

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
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
        return pl.DataFrame(rows, schema=columns, orient="row")
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
    params = []

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
            columns = [desc[0] for desc in cur.description]
        return pl.DataFrame(rows, schema=columns, orient="row")
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
        params.append(year)
    else:
        if start_year is not None:
            sql += " AND year >= %s"
            params.append(start_year)
        if end_year is not None:
            sql += " AND year <= %s"
            params.append(end_year)

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
            columns = [desc[0] for desc in cur.description]
        return pl.DataFrame(rows, schema=columns, orient="row")
    finally:
        if close_conn:
            conn.close()
