WITH counts AS (
    SELECT 'Countries' AS table_name, COUNT(*) AS count FROM wdi.countries
    UNION ALL
    SELECT 'Indicators', COUNT(*) FROM wdi.indicators
    UNION ALL
    SELECT 'Values', COUNT(*) FROM wdi.values
)
SELECT 
    table_name,
    LPAD(TO_CHAR(count, 'FM999,999,999,999'), 15, ' ') AS count
FROM counts;

