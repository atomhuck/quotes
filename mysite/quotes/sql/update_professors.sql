INSERT INTO professors(name, faculty_id)
SELECT DISTINCT ON (r.professor)
r.professor,
f.id
FROM raw_data r
INNER JOIN faculties f ON r.faculty = f.name;
