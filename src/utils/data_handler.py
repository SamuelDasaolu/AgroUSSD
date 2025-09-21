from pathlib import Path
import json, tempfile, os

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
USERS_FILE = ROOT_DIR / 'data' / 'users.json'
ORDERS_FILE = ROOT_DIR / "data" / "orders.json"


def _safe_write(path: Path, obj):
    dirpath = path.parent
    dirpath.mkdir(parents=True, exist_ok=True)
    data = json.dumps(obj, ensure_ascii=False, indent=2)
    fd, tmppath = tempfile.mkstemp(dir=str(dirpath), prefix='.tmp_', suffix='.json')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(data)
        os.replace(tmppath, str(path))
    finally:
        if os.path.exists(tmppath):
            try:
                os.remove(tmppath)
            except Exception:
                pass


def load_user_data():
    if not USERS_FILE.exists():
        return {"farmers": [], "buyers": []}
    with open(USERS_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
        if "farmers" not in data:
            data["farmers"] = []
        if "buyers" not in data:
            data["buyers"] = []
        return data


def save_user_data(data):
    # merge with existing to avoid drops
    existing = load_user_data()
    existing.update(data)
    _safe_write(USERS_FILE, existing)


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
    _safe_write(ORDERS_FILE, existing_data)


# Compatibility wrappers
def load_orders():
    return load_order_data()

def save_orders(data):
    return save_order_data(data)
