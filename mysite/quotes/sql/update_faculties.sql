INSERT INTO faculties(name)
SELECT
DISTINCT faculty
FROM raw_data
WHERE faculty IS NOT NULL;
