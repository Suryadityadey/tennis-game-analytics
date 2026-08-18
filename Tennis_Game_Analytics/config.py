import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# SportRadar configuration
SPORTRADAR_API_KEY = os.getenv("SPORTRADAR_API_KEY")

ACCESS_LEVEL = "trial"
API_VERSION = "v3"
LANGUAGE_CODE = "en"
RESPONSE_FORMAT = "json"

BASE_URL = (
    f"https://api.sportradar.com/tennis/"
    f"{ACCESS_LEVEL}/{API_VERSION}/{LANGUAGE_CODE}"
)

# Validate API key
if not SPORTRADAR_API_KEY:
    raise ValueError(
        "SPORTRADAR_API_KEY was not found in the .env file."
    )
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Surya@2026"
DB_NAME = "tennis_game_analytics"