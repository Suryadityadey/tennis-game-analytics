import json
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"
RESULTS_FILE = BASE_DIR / "data" / "processed" / "event_results.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


events = load_json(EVENTS_FILE)
results = load_json(RESULTS_FILE)


# --------------------------------------------------
# Chart 1: Events by Date
# --------------------------------------------------

events_by_date = {}

for event in events:

    date = event["start_time"][:10]

    events_by_date[date] = events_by_date.get(date, 0) + 1


dates = list(events_by_date.keys())
counts = list(events_by_date.values())


plt.figure(figsize=(8, 5))

plt.bar(dates, counts)

plt.title("Tennis Events by Date")
plt.xlabel("Date")
plt.ylabel("Number of Events")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "analysis" / "events_by_date.png"
)

plt.close()


# --------------------------------------------------
# Chart 2: Home vs Away Wins
# --------------------------------------------------

home_wins = 0
away_wins = 0


event_lookup = {
    event["event_id"]: event
    for event in events
}


for result in results:

    event = event_lookup.get(result["event_id"])

    if not event:
        continue

    if result["winner_id"] == event["home_competitor_id"]:
        home_wins += 1

    elif result["winner_id"] == event["away_competitor_id"]:
        away_wins += 1


labels = ["Home", "Away"]
wins = [home_wins, away_wins]


plt.figure(figsize=(7, 5))

plt.bar(labels, wins)

plt.title("Home vs Away Wins")
plt.xlabel("Winner Position")
plt.ylabel("Number of Wins")

plt.tight_layout()

plt.savefig(
    BASE_DIR / "analysis" / "home_vs_away_wins.png"
)

plt.close()


print("Visualization completed successfully.")

print(
    "Created:",
    "analysis/events_by_date.png"
)

print(
    "Created:",
    "analysis/home_vs_away_wins.png"
)