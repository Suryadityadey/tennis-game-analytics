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
    / "complexes_raw.json"
)


PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


COMPLEXES_FILE = (
    PROCESSED_DIR
    / "complexes.json"
)


VENUES_FILE = (
    PROCESSED_DIR
    / "venues.json"
)


# --------------------------------------------------
# Load raw JSON
# --------------------------------------------------

def load_complexes_data():

    print("Loading raw Complexes JSON...")

    with open(
        RAW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    print("JSON loaded successfully.")

    return data


# --------------------------------------------------
# Process Complexes and Venues
# --------------------------------------------------

def process_complexes(data):

    complexes = []
    venues = []

    complexes_list = data.get(
        "complexes",
        []
    )

    print(
        f"Total complexes found: "
        f"{len(complexes_list)}"
    )

    for complex_data in complexes_list:

        # ------------------------------------------
        # Complex information
        # ------------------------------------------

        complex_id = complex_data.get(
            "id"
        )

        complex_name = complex_data.get(
            "name"
        )

        # ------------------------------------------
        # Store complex
        # ------------------------------------------

        complexes.append({
            "complex_id": complex_id,
            "complex_name": complex_name
        })

        # ------------------------------------------
        # Get venues
        # ------------------------------------------

        venue_list = complex_data.get(
            "venues",
            []
        )

        for venue in venue_list:

            venues.append({
                "venue_id": venue.get("id"),
                "venue_name": venue.get("name"),
                "city_name": venue.get("city_name"),
                "country_name": venue.get(
                    "country_name"
                ),
                "country_code": venue.get(
                    "country_code"
                ),
                "timezone": venue.get(
                    "timezone"
                ),
                "complex_id": complex_id
            })

    return complexes, venues


# --------------------------------------------------
# Save processed JSON
# --------------------------------------------------

def save_processed_data(
    complexes,
    venues
):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------------
    # Save complexes
    # ----------------------------------------------

    with open(
        COMPLEXES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            complexes,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ----------------------------------------------
    # Save venues
    # ----------------------------------------------

    with open(
        VENUES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            venues,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(
        f"Complexes saved to: "
        f"{COMPLEXES_FILE}"
    )

    print(
        f"Venues saved to: "
        f"{VENUES_FILE}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    data = load_complexes_data()

    complexes, venues = process_complexes(
        data
    )

    save_processed_data(
        complexes,
        venues
    )

    print()
    print(
        "Total processed complexes:",
        len(complexes)
    )

    print(
        "Total processed venues:",
        len(venues)
    )

    print()
    print("First 5 complexes:")

    for complex_data in complexes[:5]:

        print(complex_data)

    print()
    print("First 5 venues:")

    for venue in venues[:5]:

        print(venue)