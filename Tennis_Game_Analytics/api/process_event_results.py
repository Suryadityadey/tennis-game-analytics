import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "event_results_raw.json"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "event_results.json"


def load_raw_results():

    print("Loading raw Event Results JSON...")

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("JSON loaded successfully.")

    return data


def process_results(data):

    results = []

    for item in data.get("results", []):

        result = {
            "event_id": item.get("event_id"),
            "status": item.get("status"),
            "match_status": item.get("match_status"),
            "home_score": item.get("home_score"),
            "away_score": item.get("away_score"),
            "winner_id": item.get("winner_id")
        }

        results.append(result)

    return results


def save_results(results):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print(f"\nResults saved to: {OUTPUT_FILE}")
    print(f"Total processed results: {len(results)}")

    print("\nFirst 5 results:")

    for result in results[:5]:
        print(result)


if __name__ == "__main__":

    data = load_raw_results()

    results = process_results(data)

    save_results(results)