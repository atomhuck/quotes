INSERT INTO QUOTES (text, professor_id, likes_count, reposts_count, date)
SELECT
  r.quote_text,
  p.id,
  likes,
  reposts,
  date
FROM raw_data r
INNER JOIN professors p ON p.name = r.professor;
