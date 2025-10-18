SELECT
    v.indicator_code,
    v.indicator_name,
    v.year,
    ROUND(v.value::numeric, 2) AS value
FROM wdi.values v
WHERE v.country_code = 'USA'
    AND v.indicator_code LIKE 'NY.GDP%'
    AND v.year BETWEEN 2010 AND 2020
ORDER BY v.indicator_code, v.year
LIMIT 20;

