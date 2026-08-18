import sys
from pathlib import Path
import json
import requests


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Import configuration
# --------------------------------------------------

from config import (
    SPORTRADAR_API_KEY,
    BASE_URL,
    RESPONSE_FORMAT
)


# --------------------------------------------------
# API configuration
# --------------------------------------------------

ENDPOINT = f"{BASE_URL}/competitions.{RESPONSE_FORMAT}"

HEADERS = {
    "accept": "application/json",
    "x-api-key": SPORTRADAR_API_KEY
}


# --------------------------------------------------
# Output directories
# --------------------------------------------------

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Collect Competition Data
# --------------------------------------------------

def collect_competitions():

    print("Starting Competition data collection...")
    print("Endpoint:", ENDPOINT)

    try:

        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            timeout=30
        )

        print(
            "HTTP Status Code:",
            response.status_code
        )

        # ------------------------------------------
        # Check response
        # ------------------------------------------

        if response.status_code != 200:

            print(
                "API request failed."
            )

            print(
                response.text[:500]
            )

            return None

        # ------------------------------------------
        # Convert JSON response to Python object
        # ------------------------------------------

        data = response.json()

        print(
            "JSON response received successfully."
        )

        # ------------------------------------------
        # Save raw JSON
        # ------------------------------------------

        output_file = (
            RAW_DATA_DIR /
            "competitions_raw.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Raw data saved to: {output_file}"
        )

        return data

    except requests.exceptions.Timeout:

        print(
            "ERROR: Connection to SportRadar timed out."
        )

        return None

    except requests.exceptions.ConnectionError:

        print(
            "ERROR: Could not connect to SportRadar."
        )

        return None

    except requests.exceptions.RequestException as error:

        print(
            "ERROR:",
            error
        )

        return None

    except ValueError:

        print(
            "ERROR: Response was not valid JSON."
        )

        return None


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    data = collect_competitions()

    if data is not None:

        print(
            "Competition data collection completed."
        )