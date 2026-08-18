import json
from pathlib import Path
import sys
import mysql.connector

sys.path.append(str(Path(__file__).resolve().parent.parent))

import config


BASE_DIR = Path(__file__).resolve().parent.parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"


def load_events():

    print("Loading processed Events JSON...")

    with open(EVENTS_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    print(f"Events loaded: {len(events)}")

    return events


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


def insert_events(connection, events):

    cursor = connection.cursor()

    # --------------------------------------------------
    # Insert competitors required by the events
    # --------------------------------------------------

    competitor_sql = """
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

    event_competitors = {}

    for event in events:

        home_id = event.get("home_competitor_id")
        home_name = event.get("home_competitor_name")

        away_id = event.get("away_competitor_id")
        away_name = event.get("away_competitor_name")

        if home_id:
            event_competitors[home_id] = (
                home_id,
                home_name or "Unknown",
                "Unknown",
                "UNK",
                ""
            )

        if away_id:
            event_competitors[away_id] = (
                away_id,
                away_name or "Unknown",
                "Unknown",
                "UNK",
                ""
            )

    for competitor in event_competitors.values():
        cursor.execute(competitor_sql, competitor)

    print(
        f"Event competitors processed: "
        f"{len(event_competitors)}"
    )

    # --------------------------------------------------
    # Insert events
    # --------------------------------------------------

    event_sql = """
        INSERT INTO events (
            event_id,
            start_time,
            start_time_confirmed,
            competition_id,
            competition_name,
            season_id,
            season_name,
            home_competitor_id,
            home_competitor_name,
            away_competitor_id,
            away_competitor_name,
            venue_id,
            venue_name,
            city_name,
            country_name,
            country_code,
            timezone
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            start_time = VALUES(start_time),
            start_time_confirmed = VALUES(start_time_confirmed),
            competition_id = VALUES(competition_id),
            competition_name = VALUES(competition_name),
            season_id = VALUES(season_id),
            season_name = VALUES(season_name),
            home_competitor_id = VALUES(home_competitor_id),
            home_competitor_name = VALUES(home_competitor_name),
            away_competitor_id = VALUES(away_competitor_id),
            away_competitor_name = VALUES(away_competitor_name),
            venue_id = VALUES(venue_id),
            venue_name = VALUES(venue_name),
            city_name = VALUES(city_name),
            country_name = VALUES(country_name),
            country_code = VALUES(country_code),
            timezone = VALUES(timezone)
    """

    processed = 0

    for event in events:

        start_time = event.get("start_time")

        if start_time:
            start_time = (
                start_time
                .replace("T", " ")
                .replace("+00:00", "")
            )

        values = (
            event.get("event_id"),
            start_time,
            event.get("start_time_confirmed"),

            event.get("competition_id"),
            event.get("competition_name"),

            event.get("season_id"),
            event.get("season_name"),

            event.get("home_competitor_id"),
            event.get("home_competitor_name"),

            event.get("away_competitor_id"),
            event.get("away_competitor_name"),

            event.get("venue_id"),
            event.get("venue_name"),
            event.get("city_name"),
            event.get("country_name"),
            event.get("country_code"),
            event.get("timezone")
        )

        cursor.execute(event_sql, values)

        processed += 1

    connection.commit()

    print(f"Events processed: {processed}")
    print("Events inserted successfully.")

    cursor.close()


if __name__ == "__main__":

    connection = None

    try:

        events = load_events()

        connection = connect_to_mysql()

        insert_events(connection, events)

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