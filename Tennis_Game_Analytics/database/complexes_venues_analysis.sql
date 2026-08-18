USE tennis_game_analytics;


-- 1. List all complexes along with their venues

SELECT
    c.complex_id,
    c.complex_name,
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
ORDER BY
    c.complex_name,
    v.venue_name;


-- 2. Count the number of venues in each complex

SELECT
    c.complex_id,
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
LEFT JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY
    c.complex_id,
    c.complex_name
ORDER BY
    total_venues DESC;


-- 3. Find complexes containing multiple venues

SELECT
    c.complex_id,
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY
    c.complex_id,
    c.complex_name
HAVING COUNT(v.venue_id) > 1
ORDER BY
    total_venues DESC;


-- 4. Count venues by country

SELECT
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY
    country_name
ORDER BY
    total_venues DESC;


-- 5. Count venues by city

SELECT
    city_name,
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY
    city_name,
    country_name
ORDER BY
    total_venues DESC;


-- 6. Find venues in USA

SELECT
    venue_id,
    venue_name,
    city_name,
    country_name,
    country_code,
    timezone,
    complex_id
FROM venues
WHERE country_name = 'USA'
ORDER BY
    city_name,
    venue_name;


-- 7. Find complexes that have no venues

SELECT
    c.complex_id,
    c.complex_name
FROM complexes c
LEFT JOIN venues v
    ON c.complex_id = v.complex_id
WHERE v.venue_id IS NULL;


-- 8. Analyze venue distribution by country

SELECT
    country_name,
    country_code,
    COUNT(*) AS total_venues
FROM venues
GROUP BY
    country_name,
    country_code
ORDER BY
    total_venues DESC;


-- 9. Count distinct complexes by country

SELECT
    v.country_name,
    COUNT(DISTINCT c.complex_id) AS total_complexes
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY
    v.country_name
ORDER BY
    total_complexes DESC;


-- 10. Top 10 complexes by number of venues

SELECT
    c.complex_id,
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY
    c.complex_id,
    c.complex_name
ORDER BY
    total_venues DESC
LIMIT 10;