# SportRadar JSON → MySQL Mapping

## 1. Categories Table

| SportRadar JSON Field | MySQL Column | Description |
|---|---|---|
| category.id | category_id | Unique category ID |
| category.name | category_name | Name of the category |

---

## 2. Competitions Table

| SportRadar JSON Field | MySQL Column | Description |
|---|---|---|
| competition.id | competition_id | Unique competition ID |
| competition.name | competition_name | Name of competition |
| competition.parent_id | parent_id | Parent competition ID |
| competition.type | type | Competition type |
| competition.gender | gender | Gender |
| competition.category.id | category_id | Category ID |

---

## 3. Relationship

categories.category_id
        │
        │
        ▼
competitions.category_id