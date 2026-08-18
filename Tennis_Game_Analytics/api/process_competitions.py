import json
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "competitions_raw.json"
)
PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

# --------------------------------------------------
# Load raw JSON
# --------------------------------------------------

def load_competition_data():

    print("Loading raw Competition JSON...")

    with open(
        RAW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    print("JSON loaded successfully.")

    return data


# --------------------------------------------------
# Extract Categories and Competitions
# --------------------------------------------------

def process_competitions(data):

    categories = []
    competitions = []

    # Used to prevent duplicate categories
    category_ids = set()

    competition_list = data.get(
        "competitions",
        []
    )

    print(
        f"Total competitions found: "
        f"{len(competition_list)}"
    )

    # ----------------------------------------------
    # Process each competition
    # ----------------------------------------------

    for competition in competition_list:

        # ------------------------------------------
        # Competition information
        # ------------------------------------------

        competition_id = competition.get("id")

        competition_name = competition.get(
            "name"
        )

        parent_id = competition.get(
            "parent_id"
        )

        competition_type = competition.get(
            "type"
        )

        gender = competition.get(
            "gender"
        )

        # ------------------------------------------
        # Category information
        # ------------------------------------------

        category = competition.get(
            "category",
            {}
        )

        category_id = category.get(
            "id"
        )

        category_name = category.get(
            "name"
        )

        # ------------------------------------------
        # Store unique category
        # ------------------------------------------

        if (
            category_id
            and category_id not in category_ids
        ):

            categories.append({
                "category_id": category_id,
                "category_name": category_name
            })

            category_ids.add(
                category_id
            )

        # ------------------------------------------
        # Store competition
        # ------------------------------------------

        competitions.append({
            "competition_id": competition_id,
            "competition_name": competition_name,
            "parent_id": parent_id,
            "type": competition_type,
            "gender": gender,
            "category_id": category_id
        })

    return categories, competitions
def save_processed_data(categories, competitions):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    categories_file = (
        PROCESSED_DIR
        / "categories.json"
    )

    competitions_file = (
        PROCESSED_DIR
        / "competitions.json"
    )

    with open(
        categories_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            categories,
            file,
            indent=4,
            ensure_ascii=False
        )

    with open(
        competitions_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            competitions,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(
        f"Categories saved to: {categories_file}"
    )

    print(
        f"Competitions saved to: {competitions_file}"
    )

# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    data = load_competition_data()

    categories, competitions = (
        process_competitions(data)
    )
    save_processed_data(
        categories,
        competitions
    )
    print()
    print(
        "Unique categories:",
        len(categories)
    )

    print(
        "Competitions:",
        len(competitions)
    )

    print()
    print("First 5 categories:")

    for category in categories[:5]:

        print(category)

    print()
    print("First 5 competitions:")

    for competition in competitions[:5]:

        print(competition)