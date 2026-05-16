import requests
import json
import os

BASE_URL = "https://dogapi.dog/api/v2/breeds"

RAW_FOLDER = "data/raw"
RAW_FILE = f"{RAW_FOLDER}/breeds_raw.json"


def extract_data():
    os.makedirs(RAW_FOLDER, exist_ok=True)

    response = requests.get(BASE_URL)

    if response.status_code == 200:
        data = response.json()

        with open(RAW_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"RAW guardado en: {RAW_FILE}")

    else:
        print(f"Error {response.status_code}")


if __name__ == "__main__":
    extract_data()