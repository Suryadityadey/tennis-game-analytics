import json
from pathlib import Path
import mysql.connector


PROJECT_ROOT = Path(__file__).resolve().parent.parent


CATEGORIES_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "categories.json"
)


COMPETITIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "competitions.json"
)


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Surya@2026",
    "database": "tennis_game_analytics"
}


def load_json_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def create_connection():

    return mysql.connector.connect(
        **DB_CONFIG
    )


def insert_categories(cursor, categories):

    query = """
        INSERT INTO categories (
            category_id,
            category_name
        )
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            category_name = VALUES(category_name)
    """

    for category in categories:

        cursor.execute(
            query,
            (
                category["category_id"],
                category["category_name"]
            )
        )


def insert_competitions(cursor, competitions):

    query = """
        INSERT INTO competitions (
            competition_id,
            competition_name,
            parent_id,
            type,
            gender,
            category_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            competition_name = VALUES(competition_name),
            parent_id = VALUES(parent_id),
            type = VALUES(type),
            gender = VALUES(gender),
            category_id = VALUES(category_id)
    """

    for competition in competitions:

        cursor.execute(
            query,
            (
                competition["competition_id"],
                competition["competition_name"],
                competition["parent_id"],
                competition["type"],
                competition["gender"],
                competition["category_id"]
            )
        )


if __name__ == "__main__":

    print("Loading processed JSON files...")

    categories = load_json_file(
        CATEGORIES_FILE
    )

    competitions = load_json_file(
        COMPETITIONS_FILE
    )

    print(
        f"Categories loaded: {len(categories)}"
    )

    print(
        f"Competitions loaded: {len(competitions)}"
    )

    connection = None

    try:

        connection = create_connection()

        cursor = connection.cursor()

        print("Connected to MySQL.")

        insert_categories(
            cursor,
            categories
        )

        print("Categories inserted successfully.")

        insert_competitions(
            cursor,
            competitions
        )

        print(
            "Competitions inserted successfully."
        )

        connection.commit()

        print("Transaction committed.")

    except mysql.connector.Error as error:

        print(
            "MySQL Error:",
            error
        )

        if connection:
            connection.rollback()

    finally:

        if connection:

            cursor.close()
            connection.close()

            print(
                "MySQL connection closed."
            )