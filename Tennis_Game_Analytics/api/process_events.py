import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "season_summaries_raw.json"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "events.json"


def load_season_summaries():
    print("Loading Season Summaries JSON...")

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("JSON loaded successfully.")

    return data


def process_events(data):
    summaries = data.get("summaries", [])

    events = []

    for summary in summaries:

        sport_event = summary.get("sport_event")

        if not sport_event:
            continue

        context = sport_event.get("sport_event_context", {})
        competition = context.get("competition", {})
        season = context.get("season", {})
        venue = sport_event.get("venue", {})
        competitors = sport_event.get("competitors", [])

        home_competitor = None
        away_competitor = None

        for competitor in competitors:

            if competitor.get("qualifier") == "home":
                home_competitor = competitor

            elif competitor.get("qualifier") == "away":
                away_competitor = competitor

        event = {
            "event_id": sport_event.get("id"),
            "start_time": sport_event.get("start_time"),
            "start_time_confirmed": sport_event.get(
                "start_time_confirmed"
            ),

            "competition_id": competition.get("id"),
            "competition_name": competition.get("name"),

            "season_id": season.get("id"),
            "season_name": season.get("name"),

            "home_competitor_id": (
                home_competitor.get("id")
                if home_competitor
                else None
            ),

            "home_competitor_name": (
                home_competitor.get("name")
                if home_competitor
                else None
            ),

            "away_competitor_id": (
                away_competitor.get("id")
                if away_competitor
                else None
            ),

            "away_competitor_name": (
                away_competitor.get("name")
                if away_competitor
                else None
            ),

            "venue_id": venue.get("id"),
            "venue_name": venue.get("name"),
            "city_name": venue.get("city_name"),
            "country_name": venue.get("country_name"),
            "country_code": venue.get("country_code"),
            "timezone": venue.get("timezone")
        }

        events.append(event)

    return events


def save_events(events):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            events,
            file,
            indent=2
        )

    print(f"\nEvents saved to: {OUTPUT_FILE}")
    print(f"Total processed events: {len(events)}")


if __name__ == "__main__":

    data = load_season_summaries()

    events = process_events(data)

    save_events(events)

    print("\nFirst 5 processed events:")

    for event in events[:5]:
        print(event)