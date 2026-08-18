import sys
from pathlib import Path

import requests


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Import project configuration
# --------------------------------------------------

from config import (
    SPORTRADAR_API_KEY,
    BASE_URL,
    RESPONSE_FORMAT
)


# --------------------------------------------------
# Create API URL
# --------------------------------------------------

url = f"{BASE_URL}/competitions.{RESPONSE_FORMAT}"


# --------------------------------------------------
# Request headers
# --------------------------------------------------

headers = {
    "accept": "application/json",
    "x-api-key": SPORTRADAR_API_KEY
}


# --------------------------------------------------
# Test API
# --------------------------------------------------

print("Testing SportRadar API...")
print("Endpoint:", url)

try:

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("HTTP Status Code:", response.status_code)

    if response.status_code == 200:

        print("SUCCESS: SportRadar API is working!")

        data = response.json()

        print("Response received successfully.")

        print(
            "Top-level keys:",
            list(data.keys())
        )

    elif response.status_code == 403:

        print(
            "ERROR: API authentication/access failed."
        )

    elif response.status_code == 429:

        print(
            "ERROR: API request limit exceeded."
        )

    else:

        print(
            "ERROR: API request failed."
        )

        print(
            response.text[:500]
        )


except requests.exceptions.Timeout:

    print(
        "ERROR: Connection to SportRadar timed out."
    )


except requests.exceptions.ConnectionError:

    print(
        "ERROR: Could not connect to SportRadar."
    )


except requests.exceptions.RequestException as e:

    print(
        "ERROR:",
        e
    )