import json
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"
RESULTS_FILE = BASE_DIR / "data" / "processed" / "event_results.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


events = load_json(EVENTS_FILE)
results = load_json(RESULTS_FILE)


# -----------------------------
# Basic statistics
# -----------------------------

total_events = len(events)
total_results = len(results)

competitions = Counter(
    event["competition_name"]
    for event in events
)

venues = Counter(
    event["venue_name"]
    for event in events
)

winner_ids = Counter(
    result["winner_id"]
    for result in results
)


print("=" * 50)
print("TENNIS GAME ANALYTICS - FINAL DASHBOARD")
print("=" * 50)

print("\nDATASET SUMMARY")
print("-" * 50)
print("Total Events:", total_events)
print("Completed Results:", total_results)
print("Competitions:", len(competitions))
print("Venues:", len(venues))

print("\nCOMPETITIONS")
print("-" * 50)

for name, count in competitions.items():
    print(f"{name}: {count} events")


print("\nVENUES")
print("-" * 50)

for name, count in venues.most_common():
    print(f"{name}: {count} events")


print("\nMATCH RESULTS")
print("-" * 50)

event_lookup = {
    event["event_id"]: event
    for event in events
}


for result in results:

    event = event_lookup.get(result["event_id"])

    if not event:
        continue

    print(
        f"{event['home_competitor_name']} "
        f"{result['home_score']} - "
        f"{result['away_score']} "
        f"{event['away_competitor_name']}"
    )


# -----------------------------
# Create summary chart
# -----------------------------

dates = {}

for event in events:

    date = event["start_time"][:10]

    dates[date] = dates.get(date, 0) + 1


plt.figure(figsize=(9, 5))

plt.bar(
    dates.keys(),
    dates.values()
)

plt.title("Tennis Events by Date")
plt.xlabel("Date")
plt.ylabel("Number of Events")

plt.xticks(rotation=45)

plt.tight_layout()

output_file = BASE_DIR / "analysis" / "final_events_chart.png"

plt.savefig(output_file)

plt.close()


print("\nFINAL DASHBOARD GENERATED")
print("Chart:", output_file)
print("\nProject analysis completed successfully.")