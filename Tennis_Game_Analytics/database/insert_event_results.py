import json
from pathlib import Path
import sys
import mysql.connector

sys.path.append(str(Path(__file__).resolve().parent.parent))

import config


BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "event_results.json"
)


def load_results():

    print("Loading processed Event Results JSON...")

    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    print(f"Results loaded: {len(results)}")

    return results


def connect_to_mysql():

    print("\nConnecting to MySQL...")

    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

    print("Connected to MySQL.")

    return connection


def insert_results(connection, results):

    cursor = connection.cursor()

    sql = """
        INSERT INTO event_results (
            event_id,
            status,
            match_status,
            home_score,
            away_score,
            winner_id
        )
        VALUES (
            %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            status = VALUES(status),
            match_status = VALUES(match_status),
            home_score = VALUES(home_score),
            away_score = VALUES(away_score),
            winner_id = VALUES(winner_id)
    """

    processed = 0

    for result in results:

        values = (
            result.get("event_id"),
            result.get("status"),
            result.get("match_status"),
            result.get("home_score"),
            result.get("away_score"),
            result.get("winner_id")
        )

        cursor.execute(sql, values)

        processed += 1

    connection.commit()

    print(f"Results processed: {processed}")
    print("Event results inserted successfully.")

    cursor.close()


if __name__ == "__main__":

    connection = None

    try:

        results = load_results()

        connection = connect_to_mysql()

        insert_results(connection, results)

        print("\nTransaction committed successfully.")

    except mysql.connector.Error as error:

        print(f"\nMySQL Error: {error}")

        if connection:
            connection.rollback()

        print("Transaction rolled back.")

    except Exception as error:

        print(f"\nUnexpected Error: {error}")

        if connection:
            connection.rollback()

        print("Transaction rolled back.")

    finally:

        if connection and connection.is_connected():

            connection.close()

            print("MySQL connection closed.")