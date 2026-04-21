-- 1. Tampilkan judul artikel dan nama author yang sudah dibersihkan dari kata "By"
SELECT
    title,
    TRIM(REPLACE(author, 'By', '')) AS clean_author
FROM wired_articles;

-- 2. Tampilkan 3 nama penulis yang paling sering muncul
SELECT
    TRIM(REPLACE(author, 'By', '')) AS clean_author,
    COUNT(*) AS total_articles
FROM wired_articles
GROUP BY TRIM(REPLACE(author, 'By', ''))
ORDER BY total_articles DESC
LIMIT 3;

-- 3. Cari artikel yang mengandung kata kunci "AI", "Climate", atau "Security"
SELECT
    title,
    author,
    description
FROM wired_articles
WHERE
    title LIKE '%AI%' OR description LIKE '%AI%'
    OR title LIKE '%Climate%' OR description LIKE '%Climate%'
    OR title LIKE '%Security%' OR description LIKE '%Security%';