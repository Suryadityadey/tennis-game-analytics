USE tennis_game_analytics;


-- =========================================================
-- STEP 30
-- Competitor Performance Summary
-- =========================================================

DROP VIEW IF EXISTS competitor_performance;


CREATE VIEW competitor_performance AS
SELECT
    c.competitor_id,
    c.name,
    c.country,
    c.country_code,
    c.abbreviation,

    r.`rank`,
    r.movement,
    r.points,
    r.competitions_played,

    CASE
        WHEN r.movement > 0 THEN 'Improved'
        WHEN r.movement < 0 THEN 'Dropped'
        ELSE 'No Movement'
    END AS movement_status,

    CASE
        WHEN r.`rank` <= 10 THEN 'Top 10'
        WHEN r.`rank` <= 50 THEN 'Top 50'
        WHEN r.`rank` <= 100 THEN 'Top 100'
        WHEN r.`rank` <= 250 THEN 'Top 250'
        ELSE 'Outside Top 250'
    END AS ranking_category

FROM competitors c

JOIN competitor_rankings r
    ON c.competitor_id = r.competitor_id;