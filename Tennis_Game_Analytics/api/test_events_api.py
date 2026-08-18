import sys
from pathlib import Path
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

import config


print("Testing SportRadar Seasons API...")

url = f"{config.BASE_URL}/seasons.json"

print("Endpoint:", url)

try:

    response = requests.get(
        url,
        headers={
            "x-api-key": config.SPORTRADAR_API_KEY
        },
        timeout=30
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:

        print("Seasons API connection successful.")

        data = response.json()

        print("JSON loaded successfully.")

        print("Top-level keys:")
        print(data.keys())

        print("\nFirst 10 seasons:")

        for season in data.get("seasons", [])[:10]:
            print(season)

    else:

        print("API request failed.")
        print(response.text)

except requests.exceptions.Timeout:

    print("ERROR: Connection to SportRadar timed out.")

except requests.exceptions.RequestException as e:

    print("ERROR:", e)

except Exception as e:

    print("Unexpected ERROR:", e)