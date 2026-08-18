import json
from pathlib import Path
import mysql.connector


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMPETITORS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "competitors.json"
)

RANKINGS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "competitor_rankings.json"
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

def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# Insert competitors
# --------------------------------------------------

def insert_competitors(cursor, competitors):

    query = """
        INSERT INTO competitors (
            competitor_id,
            name,
            country,
            country_code,
            abbreviation
        )
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            country = VALUES(country),
            country_code = VALUES(country_code),
            abbreviation = VALUES(abbreviation)
    """

    data = []

    for competitor in competitors:

        data.append(
            (
                competitor["competitor_id"],
                competitor["competitor_name"],
                competitor["country"],
                competitor["country_code"],
                competitor["abbreviation"]
            )
        )

    cursor.executemany(
        query,
        data
    )

    print(
        f"Competitor records processed: {len(data)}"
    )


# --------------------------------------------------
# Insert rankings
# --------------------------------------------------

def insert_rankings(cursor, rankings):

    query = """
        INSERT INTO competitor_rankings (
            `rank`,
            movement,
            points,
            competitions_played,
            competitor_id
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    data = []

    for ranking in rankings:

        data.append(
            (
                ranking["rank"],
                ranking["movement"],
                ranking["points"],
                ranking["competitions_played"],
                ranking["competitor_id"]
            )
        )

    cursor.executemany(
        query,
        data
    )

    print(
        f"Ranking records processed: {len(data)}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("Loading processed Doubles Rankings JSON...")

    competitors = load_json(
        COMPETITORS_FILE
    )

    rankings = load_json(
        RANKINGS_FILE
    )

    print(
        f"Competitors loaded: {len(competitors)}"
    )

    print(
        f"Rankings loaded: {len(rankings)}"
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
        # Insert competitors FIRST
        # ------------------------------------------

        insert_competitors(
            cursor,
            competitors
        )

        print(
            "Competitors inserted successfully."
        )

        # ------------------------------------------
        # Insert rankings SECOND
        # ------------------------------------------

        insert_rankings(
            cursor,
            rankings
        )

        print(
            "Rankings inserted successfully."
        )

        # ------------------------------------------
        # Commit
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