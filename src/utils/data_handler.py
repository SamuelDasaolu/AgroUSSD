from pathlib import Path
import json

USERS_FILE = Path("data/users.json")


def load_user_data():
    if not USERS_FILE.exists:
        return {"farmers": [], "buyers": []}
    with open(USERS_FILE, "r", encoding='utf-8') as f:
        return json.load(f)


def save_user_data(data : dict):
    existing_data = load_user_data()
    existing_data.update(data)
    with open(USERS_FILE, "w", encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
