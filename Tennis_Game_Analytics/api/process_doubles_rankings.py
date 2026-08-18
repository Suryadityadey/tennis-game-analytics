import json
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "doubles_rankings_raw.json"
)

PROCESSED_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

RANKINGS_FILE = (
    PROCESSED_DIR
    / "competitor_rankings.json"
)

COMPETITORS_FILE = (
    PROCESSED_DIR
    / "competitors.json"
)


# --------------------------------------------------
# LOAD RAW JSON
# --------------------------------------------------

def load_raw_data():

    print("Loading raw Doubles Rankings JSON...")

    with open(
        RAW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    print("JSON loaded successfully.")

    return data


# --------------------------------------------------
# PROCESS DATA
# --------------------------------------------------

def process_data(data):

    rankings = data.get("rankings", [])

    print(
        f"Total ranking groups found: "
        f"{len(rankings)}"
    )

    competitors = []
    competitor_rankings = []

    # Used to avoid duplicate competitors
    seen_competitors = set()

    # Process every ranking group
    for ranking_group in rankings:

        type_id = ranking_group.get("type_id")
        ranking_name = ranking_group.get("name")
        year = ranking_group.get("year")
        week = ranking_group.get("week")
        gender = ranking_group.get("gender")

        ranking_records = ranking_group.get(
            "competitor_rankings",
            []
        )

        print(
            f"Processing {ranking_name}: "
            f"{len(ranking_records)} competitors"
        )

        # Process every competitor ranking
        for record in ranking_records:

            competitor = record.get(
                "competitor",
                {}
            )

            competitor_id = competitor.get("id")

            # --------------------------------------
            # COMPETITOR
            # --------------------------------------

            if (
                competitor_id
                and competitor_id not in seen_competitors
            ):

                competitors.append({
                    "competitor_id": competitor_id,
                    "competitor_name": competitor.get(
                        "name"
                    ),
                    "country": competitor.get(
                        "country"
                    ),
                    "country_code": competitor.get(
                        "country_code"
                    ),
                    "abbreviation": competitor.get(
                        "abbreviation"
                    )
                })

                seen_competitors.add(
                    competitor_id
                )

            # --------------------------------------
            # RANKING
            # --------------------------------------

            competitor_rankings.append({
                "rank": record.get("rank"),
                "movement": record.get("movement"),
                "points": record.get("points"),
                "competitions_played": record.get(
                    "competitions_played"
                ),
                "competitor_id": competitor_id
            })

    return competitors, competitor_rankings


# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

def save_json(file_path, data):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    data = load_raw_data()

    competitors, competitor_rankings = process_data(
        data
    )

    # Save competitors
    save_json(
        COMPETITORS_FILE,
        competitors
    )

    print(
        f"\nCompetitors saved to: "
        f"{COMPETITORS_FILE}"
    )

    # Save rankings
    save_json(
        RANKINGS_FILE,
        competitor_rankings
    )

    print(
        f"Rankings saved to: "
        f"{RANKINGS_FILE}"
    )

    # Statistics
    print(
        f"\nTotal ranking records: "
        f"{len(competitor_rankings)}"
    )

    print(
        f"Unique competitors: "
        f"{len(competitors)}"
    )

    # First 5 competitors
    print("\nFirst 5 competitors:")

    for competitor in competitors[:5]:
        print(competitor)

    # First 5 rankings
    print("\nFirst 5 rankings:")

    for ranking in competitor_rankings[:5]:
        print(ranking)