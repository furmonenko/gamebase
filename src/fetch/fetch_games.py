import os
import requests
import json
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
if not API_KEY:
    raise ValueError("RAWG_API_KEY is not set in the .env file.")

BASE_URL = "https://api.rawg.io/api/games"
OUTPUT_DIR = Path("../../data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Parameters
NUM_PAGES = 10  # Change this to fetch more pages
PAGE_SIZE = 40

for page in range(1, NUM_PAGES + 1):
    params = {
        "key": API_KEY,
        "page": page,
        "page_size": PAGE_SIZE,
        "dates": "2000-01-01,2024-12-31",
        "ordering": "-rating"
    }
    try:
        print(f"Fetching page {page}...")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        output_file = OUTPUT_DIR / f"games_page_{page}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Saved: {output_file}")

        sleep(1)  # Be polite to API server

    except Exception as e:
        print(f"Error on page {page}: {e}")
        break
