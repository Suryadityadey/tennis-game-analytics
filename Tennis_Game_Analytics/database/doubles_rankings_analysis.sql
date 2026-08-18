USE tennis_game_analytics;


-- =========================================================
-- 1. Top 20 Doubles Ranked Competitors
-- =========================================================

SELECT
    r.`rank`,
    c.name,
    c.country,
    r.points,
    r.competitions_played
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
ORDER BY
    r.`rank`,
    r.points DESC
LIMIT 20;


-- =========================================================
-- 2. Top 10 Competitors by Ranking Points
-- =========================================================

SELECT
    c.name,
    c.country,
    r.`rank`,
    r.points,
    r.competitions_played
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
ORDER BY
    r.points DESC
LIMIT 10;


-- =========================================================
-- 3. Competitors by Country
-- =========================================================

SELECT
    c.country,
    COUNT(*) AS total_competitors
FROM competitors c
GROUP BY
    c.country
ORDER BY
    total_competitors DESC;


-- =========================================================
-- 4. Average Ranking Points by Country
-- =========================================================

SELECT
    c.country,
    COUNT(*) AS total_competitors,
    ROUND(AVG(r.points), 2) AS average_points,
    MAX(r.points) AS highest_points
FROM competitors c
JOIN competitor_rankings r
    ON c.competitor_id = r.competitor_id
GROUP BY
    c.country
ORDER BY
    average_points DESC;


-- =========================================================
-- 5. Most Competitions Played
-- =========================================================

SELECT
    c.name,
    c.country,
    r.`rank`,
    r.points,
    r.competitions_played
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
ORDER BY
    r.competitions_played DESC
LIMIT 10;


-- =========================================================
-- 6. Ranking Movement Analysis
-- =========================================================

SELECT
    CASE
        WHEN movement > 0 THEN 'Improved'
        WHEN movement < 0 THEN 'Dropped'
        ELSE 'No Movement'
    END AS movement_status,
    COUNT(*) AS total_competitors
FROM competitor_rankings
GROUP BY
    movement_status
ORDER BY
    total_competitors DESC;


-- =========================================================
-- 7. Biggest Ranking Improvements
-- =========================================================

SELECT
    c.name,
    c.country,
    r.`rank`,
    r.movement,
    r.points
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.movement > 0
ORDER BY
    r.movement DESC
LIMIT 10;


-- =========================================================
-- 8. Biggest Ranking Drops
-- =========================================================

SELECT
    c.name,
    c.country,
    r.`rank`,
    r.movement,
    r.points
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.movement < 0
ORDER BY
    r.movement ASC
LIMIT 10;


-- =========================================================
-- 9. Competitors with No Ranking Movement
-- =========================================================

SELECT
    COUNT(*) AS unchanged_competitors
FROM competitor_rankings
WHERE movement = 0;


-- =========================================================
-- 10. Overall Ranking Statistics
-- =========================================================

SELECT
    COUNT(*) AS total_rankings,
    MIN(`rank`) AS best_rank,
    MAX(`rank`) AS lowest_rank,
    ROUND(AVG(`rank`), 2) AS average_rank,
    MIN(points) AS minimum_points,
    MAX(points) AS maximum_points,
    ROUND(AVG(points), 2) AS average_points,
    ROUND(AVG(competitions_played), 2) AS average_competitions_played
FROM competitor_rankings;


-- =========================================================
-- 11. Top Competitor from Each Country
-- =========================================================

SELECT
    c.country,
    c.name,
    r.`rank`,
    r.points
FROM competitors c
JOIN competitor_rankings r
    ON c.competitor_id = r.competitor_id
WHERE r.`rank` = (
    SELECT MIN(r2.`rank`)
    FROM competitors c2
    JOIN competitor_rankings r2
        ON c2.competitor_id = r2.competitor_id
    WHERE c2.country = c.country
)
ORDER BY
    r.`rank`,
    c.country;


-- =========================================================
-- 12. Competitors with More Than 20 Competitions Played
-- =========================================================

SELECT
    c.name,
    c.country,
    r.`rank`,
    r.points,
    r.competitions_played
FROM competitor_rankings r
JOIN competitors c
    ON r.competitor_id = c.competitor_id
WHERE r.competitions_played > 20
ORDER BY
    r.competitions_played DESC;