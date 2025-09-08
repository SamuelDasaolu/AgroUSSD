from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
USERS_FILE = ROOT_DIR / 'data' / 'users.json'
ORDERS_FILE = ROOT_DIR / "data" / "orders.json"


def load_user_data():
    if not USERS_FILE.exists():
        return {"farmers": [], "buyers": []}
    with open(USERS_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
        # Ensure both keys always exist
        if "farmers" not in data:
            data["farmers"] = []
        if "buyers" not in data:
            data["buyers"] = []

        return data


def save_user_data(data: dict):
    existing_data = load_user_data()
    existing_data.update(data)
    with open(USERS_FILE, "w", encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)


def load_order_data():
    if not ORDERS_FILE.exists():
        return {"orders": []}
    with open(ORDERS_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
    if "orders" not in data:
        data["orders"] = []
    return data


def save_order_data(data):
    existing_data = load_order_data()
    existing_data.update(data)
    with open(ORDERS_FILE, "w", encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
