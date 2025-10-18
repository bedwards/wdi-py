SELECT 'Countries without region' as check_name, COUNT(*) as count 
FROM wdi.countries 
WHERE region IS NULL OR region = '';

