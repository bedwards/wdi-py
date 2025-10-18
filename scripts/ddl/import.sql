-- ============================================================================
-- World Bank Development Indicators (WDI) PostgreSQL Import Script
-- Clean schema with only countries, indicators, and values tables
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS wdi;

-- ============================================================================
-- STAGING TABLES
-- ============================================================================

-- Staging table for WDICountry.csv
CREATE TEMP TABLE country_staging (
    country_code VARCHAR(3),
    short_name TEXT,
    table_name TEXT,
    long_name TEXT,
    alpha_2_code VARCHAR(2),
    currency_unit TEXT,
    special_notes TEXT,
    region TEXT,
    income_group TEXT,
    wb_2_code VARCHAR(2),
    national_accounts_base_year TEXT,
    national_accounts_reference_year TEXT,
    sna_price_valuation TEXT,
    lending_category TEXT,
    other_groups TEXT,
    system_of_national_accounts TEXT,
    alternative_conversion_factor TEXT,
    ppp_survey_year TEXT,
    balance_of_payments_manual_in_use TEXT,
    external_debt_reporting_status TEXT,
    system_of_trade TEXT,
    government_accounting_concept TEXT,
    imf_data_dissemination_standard TEXT,
    latest_population_census TEXT,
    latest_household_survey TEXT,
    source_of_most_recent_income_and_expenditure_data TEXT,
    vital_registration_complete TEXT,
    latest_agricultural_census TEXT,
    latest_industrial_data TEXT,
    latest_trade_data TEXT,
    latest_water_withdrawal_data TEXT
);

-- Staging table for WDISeries.csv
CREATE TEMP TABLE series_staging (
    series_code VARCHAR(50),
    topic TEXT,
    indicator_name TEXT,
    short_definition TEXT,
    long_definition TEXT,
    unit_of_measure TEXT,
    periodicity TEXT,
    base_period TEXT,
    other_notes TEXT,
    aggregation_method TEXT,
    limitations_and_exceptions TEXT,
    notes_from_original_source TEXT,
    general_comments TEXT,
    source TEXT,
    statistical_concept_and_methodology TEXT,
    development_relevance TEXT,
    related_source_links TEXT,
    other_web_links TEXT,
    related_indicators TEXT,
    license_type TEXT
);

-- Staging table for WDICSV.csv (wide format with year columns)
CREATE TEMP TABLE data_staging (
    country_name TEXT,
    country_code VARCHAR(3),
    indicator_name TEXT,
    indicator_code VARCHAR(50),
    "1960" NUMERIC, "1961" NUMERIC, "1962" NUMERIC, "1963" NUMERIC, "1964" NUMERIC,
    "1965" NUMERIC, "1966" NUMERIC, "1967" NUMERIC, "1968" NUMERIC, "1969" NUMERIC,
    "1970" NUMERIC, "1971" NUMERIC, "1972" NUMERIC, "1973" NUMERIC, "1974" NUMERIC,
    "1975" NUMERIC, "1976" NUMERIC, "1977" NUMERIC, "1978" NUMERIC, "1979" NUMERIC,
    "1980" NUMERIC, "1981" NUMERIC, "1982" NUMERIC, "1983" NUMERIC, "1984" NUMERIC,
    "1985" NUMERIC, "1986" NUMERIC, "1987" NUMERIC, "1988" NUMERIC, "1989" NUMERIC,
    "1990" NUMERIC, "1991" NUMERIC, "1992" NUMERIC, "1993" NUMERIC, "1994" NUMERIC,
    "1995" NUMERIC, "1996" NUMERIC, "1997" NUMERIC, "1998" NUMERIC, "1999" NUMERIC,
    "2000" NUMERIC, "2001" NUMERIC, "2002" NUMERIC, "2003" NUMERIC, "2004" NUMERIC,
    "2005" NUMERIC, "2006" NUMERIC, "2007" NUMERIC, "2008" NUMERIC, "2009" NUMERIC,
    "2010" NUMERIC, "2011" NUMERIC, "2012" NUMERIC, "2013" NUMERIC, "2014" NUMERIC,
    "2015" NUMERIC, "2016" NUMERIC, "2017" NUMERIC, "2018" NUMERIC, "2019" NUMERIC,
    "2020" NUMERIC, "2021" NUMERIC, "2022" NUMERIC, "2023" NUMERIC, "2024" NUMERIC
);

-- ============================================================================
-- LOAD DATA INTO STAGING TABLES
-- ============================================================================

COPY country_staging FROM '/workspace/WDI_CSV/WDICountry.csv' 
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COPY series_staging FROM '/workspace/WDI_CSV/WDISeries.csv' 
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COPY data_staging FROM '/workspace/WDI_CSV/WDICSV.csv' 
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- ============================================================================
-- CREATE FINAL TABLES
-- ============================================================================

-- Countries table: only actual countries with regions (no rollups/aggregates)
CREATE TABLE wdi.countries (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) UNIQUE NOT NULL,
    country_name TEXT NOT NULL,
    region TEXT NOT NULL,
    income_group TEXT
);

-- Determine which name field matches data_staging.country_name
-- In WDI data, table_name typically matches the country_name used in WDICSV
INSERT INTO wdi.countries (country_code, country_name, region, income_group)
SELECT DISTINCT
    cs.country_code,
    cs.table_name as country_name,
    cs.region,
    cs.income_group
FROM country_staging cs
WHERE cs.region IS NOT NULL 
    AND cs.region != ''
    AND cs.country_code IN (SELECT DISTINCT country_code FROM data_staging);

-- Indicators table: get indicator_code from WDICSV, metadata from WDISeries
CREATE TABLE wdi.indicators (
    id SERIAL PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE NOT NULL,
    indicator_name TEXT NOT NULL,
    topic TEXT,
    short_definition TEXT,
    long_definition TEXT,
    unit_of_measure TEXT,
    periodicity TEXT,
    base_period TEXT,
    other_notes TEXT,
    aggregation_method TEXT,
    limitations_and_exceptions TEXT,
    notes_from_original_source TEXT,
    general_comments TEXT,
    source TEXT,
    statistical_concept_and_methodology TEXT,
    development_relevance TEXT,
    related_source_links TEXT,
    other_web_links TEXT,
    related_indicators TEXT,
    license_type TEXT
);

-- Join WDICSV indicators with WDISeries on indicator_name to get metadata
INSERT INTO wdi.indicators (
    indicator_code, indicator_name, topic, short_definition, long_definition,
    unit_of_measure, periodicity, base_period, other_notes, aggregation_method,
    limitations_and_exceptions, notes_from_original_source, general_comments,
    source, statistical_concept_and_methodology, development_relevance,
    related_source_links, other_web_links, related_indicators, license_type
)
SELECT DISTINCT
    ds.indicator_code,
    ds.indicator_name,
    ss.topic,
    ss.short_definition,
    ss.long_definition,
    ss.unit_of_measure,
    ss.periodicity,
    ss.base_period,
    ss.other_notes,
    ss.aggregation_method,
    ss.limitations_and_exceptions,
    ss.notes_from_original_source,
    ss.general_comments,
    ss.source,
    ss.statistical_concept_and_methodology,
    ss.development_relevance,
    ss.related_source_links,
    ss.other_web_links,
    ss.related_indicators,
    ss.license_type
FROM data_staging ds
LEFT JOIN series_staging ss ON ds.indicator_name = ss.indicator_name
WHERE ds.indicator_code IN (
    SELECT DISTINCT indicator_code 
    FROM data_staging 
    WHERE country_code IN (SELECT country_code FROM wdi.countries)
);

-- Values table: normalized long format with only actual country data
CREATE TABLE wdi.values (
    id BIGSERIAL PRIMARY KEY,
    country_code VARCHAR(3) NOT NULL,
    country_name TEXT NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    value NUMERIC,
    CONSTRAINT fk_values_country FOREIGN KEY (country_code) 
        REFERENCES wdi.countries(country_code),
    CONSTRAINT fk_values_indicator FOREIGN KEY (indicator_code) 
        REFERENCES wdi.indicators(indicator_code),
    CONSTRAINT unique_country_indicator_year UNIQUE (country_code, indicator_code, year)
);

-- Transform wide format to long format, filtering for actual countries only
INSERT INTO wdi.values (country_code, country_name, indicator_code, indicator_name, year, value)
SELECT 
    ds.country_code,
    c.country_name,
    ds.indicator_code,
    ds.indicator_name,
    year::integer,
    value
FROM data_staging ds
INNER JOIN wdi.countries c ON ds.country_code = c.country_code
CROSS JOIN LATERAL (
    VALUES
        ('1960', ds."1960"), ('1961', ds."1961"), ('1962', ds."1962"), ('1963', ds."1963"), ('1964', ds."1964"),
        ('1965', ds."1965"), ('1966', ds."1966"), ('1967', ds."1967"), ('1968', ds."1968"), ('1969', ds."1969"),
        ('1970', ds."1970"), ('1971', ds."1971"), ('1972', ds."1972"), ('1973', ds."1973"), ('1974', ds."1974"),
        ('1975', ds."1975"), ('1976', ds."1976"), ('1977', ds."1977"), ('1978', ds."1978"), ('1979', ds."1979"),
        ('1980', ds."1980"), ('1981', ds."1981"), ('1982', ds."1982"), ('1983', ds."1983"), ('1984', ds."1984"),
        ('1985', ds."1985"), ('1986', ds."1986"), ('1987', ds."1987"), ('1988', ds."1988"), ('1989', ds."1989"),
        ('1990', ds."1990"), ('1991', ds."1991"), ('1992', ds."1992"), ('1993', ds."1993"), ('1994', ds."1994"),
        ('1995', ds."1995"), ('1996', ds."1996"), ('1997', ds."1997"), ('1998', ds."1998"), ('1999', ds."1999"),
        ('2000', ds."2000"), ('2001', ds."2001"), ('2002', ds."2002"), ('2003', ds."2003"), ('2004', ds."2004"),
        ('2005', ds."2005"), ('2006', ds."2006"), ('2007', ds."2007"), ('2008', ds."2008"), ('2009', ds."2009"),
        ('2010', ds."2010"), ('2011', ds."2011"), ('2012', ds."2012"), ('2013', ds."2013"), ('2014', ds."2014"),
        ('2015', ds."2015"), ('2016', ds."2016"), ('2017', ds."2017"), ('2018', ds."2018"), ('2019', ds."2019"),
        ('2020', ds."2020"), ('2021', ds."2021"), ('2022', ds."2022"), ('2023', ds."2023"), ('2024', ds."2024")
) AS years(year, value)
WHERE value IS NOT NULL;

-- ============================================================================
-- CREATE INDEXES
-- ============================================================================

-- Indexes to support joins on country_code and indicator_code
CREATE INDEX idx_countries_code ON wdi.countries(country_code);
CREATE INDEX idx_indicators_code ON wdi.indicators(indicator_code);

-- Indexes to support filtering values by country_code, indicator_code, and year
CREATE INDEX idx_values_country ON wdi.values(country_code);
CREATE INDEX idx_values_indicator ON wdi.values(indicator_code);
CREATE INDEX idx_values_year ON wdi.values(year);
CREATE INDEX idx_values_country_indicator ON wdi.values(country_code, indicator_code);
CREATE INDEX idx_values_country_year ON wdi.values(country_code, year);
CREATE INDEX idx_values_indicator_year ON wdi.values(indicator_code, year);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check record counts
SELECT 'Countries' as table_name, COUNT(*) as count FROM wdi.countries
UNION ALL
SELECT 'Indicators', COUNT(*) FROM wdi.indicators
UNION ALL
SELECT 'Values', COUNT(*) FROM wdi.values;

-- Verify all countries have regions
SELECT 'Countries without region' as check_name, COUNT(*) as count 
FROM wdi.countries 
WHERE region IS NULL OR region = '';

-- Sample query: GDP data for USA
SELECT
    v.country_name,
    v.indicator_name,
    v.year,
    v.value
FROM wdi.values v
WHERE v.country_code = 'USA'
    AND v.indicator_code LIKE 'NY.GDP%'
    AND v.year BETWEEN 2010 AND 2020
ORDER BY v.indicator_code, v.year
LIMIT 20;