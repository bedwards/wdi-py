"""Tests for wdi.sql module."""

import pytest
from unittest.mock import Mock, patch
import polars as pl
from wdi import sql


@pytest.fixture
def mock_connection() -> Mock:
    """Create a mock database connection."""
    conn = Mock()
    conn.cursor.return_value.__enter__ = Mock(return_value=conn.cursor.return_value)
    conn.cursor.return_value.__exit__ = Mock(return_value=False)
    return conn


def test_get_connection_default_params() -> None:
    """Test get_connection with default parameters."""
    with patch("psycopg2.connect") as mock_connect:
        sql.get_connection()
        mock_connect.assert_called_once_with(
            host="localhost",
            port=5432,
            database="db",
            user="postgres",
        )


def test_get_connection_with_password() -> None:
    """Test get_connection with password."""
    with patch("psycopg2.connect") as mock_connect:
        sql.get_connection(password="secret")
        mock_connect.assert_called_once_with(
            host="localhost",
            port=5432,
            database="db",
            user="postgres",
            password="secret",
        )


def test_query_with_connection(mock_connection: Mock) -> None:
    """Test query with provided connection."""
    with patch("polars.read_database") as mock_read:
        mock_read.return_value = pl.DataFrame({"a": [1, 2, 3]})
        result = sql.query("SELECT * FROM test", conn=mock_connection)
        assert isinstance(result, pl.DataFrame)
        mock_read.assert_called_once_with("SELECT * FROM test", mock_connection)


def test_query_creates_connection_if_none() -> None:
    """Test query creates connection if none provided."""
    with patch("wdi.sql.get_connection") as mock_get_conn, \
         patch("polars.read_database") as mock_read:
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn
        mock_read.return_value = pl.DataFrame({"a": [1, 2, 3]})
        
        result = sql.query("SELECT * FROM test")
        
        assert isinstance(result, pl.DataFrame)
        mock_get_conn.assert_called_once()
        mock_conn.close.assert_called_once()


def test_get_countries_no_filters(mock_connection: Mock) -> None:
    """Test get_countries without filters."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        ("USA", "United States", "North America", "High income"),
        ("CHN", "China", "East Asia & Pacific", "Upper middle income"),
    ]
    cursor_mock.description = [
        ("country_code",), ("country_name",), ("region",), ("income_group",)
    ]
    
    result = sql.get_countries(conn=mock_connection)
    
    assert isinstance(result, pl.DataFrame)
    assert len(result) == 2
    assert "country_code" in result.columns


def test_get_countries_with_region_filter(mock_connection: Mock) -> None:
    """Test get_countries with region filter."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        ("USA", "United States", "North America", "High income"),
    ]
    cursor_mock.description = [
        ("country_code",), ("country_name",), ("region",), ("income_group",)
    ]
    
    result = sql.get_countries(region="North America", conn=mock_connection)
    
    cursor_mock.execute.assert_called_once()
    sql_call = cursor_mock.execute.call_args[0][0]
    assert "region = %s" in sql_call


def test_get_indicators_no_filters(mock_connection: Mock) -> None:
    """Test get_indicators without filters."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        ("NY.GDP.MKTP.CD", "GDP (current US$)", "Economy", "GDP at purchaser's prices"),
    ]
    cursor_mock.description = [
        ("indicator_code",), ("indicator_name",), ("topic",), ("short_definition",)
    ]
    
    result = sql.get_indicators(conn=mock_connection)
    
    assert isinstance(result, pl.DataFrame)
    assert "indicator_code" in result.columns


def test_get_indicators_with_search(mock_connection: Mock) -> None:
    """Test get_indicators with search term."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = []
    cursor_mock.description = [("indicator_code",), ("indicator_name",)]
    
    sql.get_indicators(search="GDP", conn=mock_connection)
    
    cursor_mock.execute.assert_called_once()
    sql_call = cursor_mock.execute.call_args[0][0]
    assert "LOWER(indicator_name) LIKE LOWER(%s)" in sql_call


def test_get_values_basic(mock_connection: Mock) -> None:
    """Test get_values with indicator code."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        (1, "USA", "United States", "NY.GDP.MKTP.CD", "GDP", 2020, 21000000000000),
    ]
    cursor_mock.description = [
        ("id",), ("country_code",), ("country_name",), 
        ("indicator_code",), ("indicator_name",), ("year",), ("value",)
    ]
    
    result = sql.get_values("NY.GDP.MKTP.CD", conn=mock_connection)
    
    assert isinstance(result, pl.DataFrame)
    cursor_mock.execute.assert_called_once()


def test_get_values_with_year_filter(mock_connection: Mock) -> None:
    """Test get_values with year filter."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = []
    cursor_mock.description = [("country_code",), ("year",), ("value",)]
    
    sql.get_values("NY.GDP.MKTP.CD", year=2020, conn=mock_connection)
    
    sql_call = cursor_mock.execute.call_args[0][0]
    assert "year = %s" in sql_call


def test_get_values_with_year_range(mock_connection: Mock) -> None:
    """Test get_values with year range."""
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = []
    cursor_mock.description = [("year",), ("value",)]
    
    sql.get_values(
        "NY.GDP.MKTP.CD", 
        start_year=2010, 
        end_year=2020, 
        conn=mock_connection
    )
    
    sql_call = cursor_mock.execute.call_args[0][0]
    assert "year >= %s" in sql_call
    assert "year <= %s" in sql_call