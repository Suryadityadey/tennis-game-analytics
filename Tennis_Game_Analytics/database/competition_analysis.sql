USE tennis_game_analytics;


-- 1. List all competitions along with their category name

SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id;


-- 2. Count the number of competitions in each category

SELECT
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM categories cat
LEFT JOIN competitions c
    ON cat.category_id = c.category_id
GROUP BY
    cat.category_id,
    cat.category_name;


-- 3. Find all competitions of type 'doubles'

SELECT
    competition_id,
    competition_name,
    gender,
    category_id
FROM competitions
WHERE type = 'doubles';


-- 4. Get competitions belonging to a specific category

SELECT
    c.competition_id,
    c.competition_name,
    c.type,
    c.gender,
    cat.category_name
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';


-- 5. Identify parent competitions and their sub-competitions

SELECT
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM competitions child
JOIN competitions parent
    ON child.parent_id = parent.competition_id;


-- 6. Analyze the distribution of competition types by category

SELECT
    cat.category_name,
    c.type,
    COUNT(*) AS total_competitions
FROM competitions c
JOIN categories cat
    ON c.category_id = cat.category_id
GROUP BY
    cat.category_id,
    cat.category_name,
    c.type
ORDER BY
    cat.category_name,
    c.type;


-- 7. List all competitions with no parent

SELECT
    competition_id,
    competition_name,
    type,
    gender,
    category_id
FROM competitions
WHERE parent_id IS NULL;