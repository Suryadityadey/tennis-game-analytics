import json
from pathlib import Path
import mysql.connector


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


COMPLEXES_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "complexes.json"
)


VENUES_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "venues.json"
)


# --------------------------------------------------
# MySQL configuration
# --------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Surya@2026",
    "database": "tennis_game_analytics"
}


# --------------------------------------------------
# Load JSON
# --------------------------------------------------

def load_json_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# Insert complexes
# --------------------------------------------------

def insert_complexes(cursor, complexes):

    query = """
        INSERT INTO complexes (
            complex_id,
            complex_name
        )
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            complex_name = VALUES(complex_name)
    """

    data = []

    for complex_data in complexes:

        data.append(
            (
                complex_data["complex_id"],
                complex_data["complex_name"]
            )
        )

    cursor.executemany(
        query,
        data
    )

    print(
        f"Complex records processed: {len(data)}"
    )


# --------------------------------------------------
# Insert venues
# --------------------------------------------------

def insert_venues(cursor, venues):

    query = """
        INSERT INTO venues (
            venue_id,
            venue_name,
            city_name,
            country_name,
            country_code,
            timezone,
            complex_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            venue_name = VALUES(venue_name),
            city_name = VALUES(city_name),
            country_name = VALUES(country_name),
            country_code = VALUES(country_code),
            timezone = VALUES(timezone),
            complex_id = VALUES(complex_id)
    """

    data = []

    for venue in venues:

        data.append(
            (
                venue["venue_id"],
                venue["venue_name"],
                venue["city_name"],
                venue["country_name"],
                venue["country_code"],
                venue["timezone"],
                venue["complex_id"]
            )
        )

    cursor.executemany(
        query,
        data
    )

    print(
        f"Venue records processed: {len(data)}"
    )


# --------------------------------------------------
# Main program
# --------------------------------------------------

if __name__ == "__main__":

    print("Loading processed Complexes JSON...")
    
    complexes = load_json_file(
        COMPLEXES_FILE
    )

    print("Loading processed Venues JSON...")

    venues = load_json_file(
        VENUES_FILE
    )

    print()
    print(
        f"Complexes loaded: {len(complexes)}"
    )

    print(
        f"Venues loaded: {len(venues)}"
    )

    connection = None

    try:

        print()
        print("Connecting to MySQL...")

        connection = mysql.connector.connect(
            **DB_CONFIG
        )

        cursor = connection.cursor()

        print("Connected to MySQL.")

        # ------------------------------------------
        # Insert complexes first
        # ------------------------------------------

        insert_complexes(
            cursor,
            complexes
        )

        print(
            "Complexes inserted successfully."
        )

        # ------------------------------------------
        # Insert venues second
        # ------------------------------------------

        insert_venues(
            cursor,
            venues
        )

        print(
            "Venues inserted successfully."
        )

        # ------------------------------------------
        # Commit transaction
        # ------------------------------------------

        connection.commit()

        print()
        print(
            "Transaction committed successfully."
        )

    except mysql.connector.Error as error:

        print()
        print(
            "MySQL Error:",
            error
        )

        if connection:
            connection.rollback()

            print(
                "Transaction rolled back."
            )

    except Exception as error:

        print()
        print(
            "Error:",
            error
        )

        if connection:
            connection.rollback()

            print(
                "Transaction rolled back."
            )

    finally:

        if connection:

            cursor.close()
            connection.close()

            print(
                "MySQL connection closed."
            )