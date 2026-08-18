import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"
RESULTS_FILE = BASE_DIR / "data" / "processed" / "event_results.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():

    print("Loading project data...")

    events = load_json(EVENTS_FILE)
    results = load_json(RESULTS_FILE)

    print("Data loaded successfully.\n")

    print("===== DATASET SUMMARY =====")
    print("Total events:", len(events))
    print("Total results:", len(results))

    competitions = Counter(
        event["competition_name"]
        for event in events
    )

    print("\n===== EVENTS BY COMPETITION =====")

    for competition, count in competitions.items():
        print(f"{competition}: {count}")

    winners = Counter(
        result["winner_id"]
        for result in results
    )

    print("\n===== WINNER IDs =====")

    for winner, count in winners.items():
        print(f"{winner}: {count} win(s)")

    print("\n===== MATCH RESULTS =====")

    for result in results:

        event_id = result["event_id"]

        matching_events = [
            event for event in events
            if event["event_id"] == event_id
        ]

        if not matching_events:
            continue

        event = matching_events[0]

        print(
            f"{event['home_competitor_name']} "
            f"{result['home_score']} - "
            f"{result['away_score']} "
            f"{event['away_competitor_name']}"
        )

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()