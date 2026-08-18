import json
import time
from pathlib import Path

import requests

import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import config


BASE_DIR = Path(__file__).resolve().parent.parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "event_results_raw.json"


def load_events():

    print("Loading processed Events JSON...")

    with open(EVENTS_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    print(f"Total events found: {len(events)}")

    return events


def load_existing_results():

    if not OUTPUT_FILE.exists():
        return []

    try:

        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("results", [])

    except (json.JSONDecodeError, KeyError):

        return []


def fetch_event_result(event_id):

    url = (
        f"{config.BASE_URL}"
        f"/sport_events/{event_id}/summary.json"
    )

    headers = {
        "accept": "application/json"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params={
                "api_key": config.SPORTRADAR_API_KEY
            },
            timeout=30
        )

        if response.status_code == 200:

            return response.json()

        print(
            f"HTTP {response.status_code} "
            f"for {event_id}"
        )

        return None

    except requests.exceptions.Timeout:

        print(f"Timeout for {event_id}")
        return None

    except requests.exceptions.RequestException as error:

        print(f"Request error for {event_id}: {error}")
        return None


def extract_result(data):

    sport_event = data.get("sport_event", {})
    status = data.get("sport_event_status", {})

    event_id = sport_event.get("id")

    if not event_id:
        return None

    return {
        "event_id": event_id,
        "status": status.get("status"),
        "match_status": status.get("match_status"),
        "home_score": status.get("home_score"),
        "away_score": status.get("away_score"),
        "winner_id": status.get("winner_id")
    }


def main():

    events = load_events()

    existing_results = load_existing_results()

    existing_ids = {
        result.get("event_id")
        for result in existing_results
    }

    print(
        f"Existing results: "
        f"{len(existing_results)}"
    )

    results = existing_results.copy()

    for index, event in enumerate(events, start=1):

        event_id = event.get("event_id")

        if not event_id:
            continue

        if event_id in existing_ids:

            print(
                f"[{index}/{len(events)}] "
                f"Already collected: {event_id}"
            )

            continue

        print(
            f"[{index}/{len(events)}] "
            f"Fetching: {event_id}"
        )

        data = fetch_event_result(event_id)

        if data:

            result = extract_result(data)

            if result:

                results.append(result)
                existing_ids.add(event_id)

                print(
                    f"  Success: "
                    f"{result['home_score']} - "
                    f"{result['away_score']}"
                )

            else:

                print("  Could not extract result.")

        time.sleep(1)

    output_data = {
        "results": results
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=2
        )

    print("\nCollection completed.")
    print(f"Total results saved: {len(results)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    