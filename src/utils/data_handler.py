from pathlib import Path
import json, tempfile

ROOT = Path(__file__).resolve().parent.parent.parent
USERS_FILE = ROOT / 'data' / 'users.json'
ORDERS_FILE = ROOT / 'data' / 'orders.json'

def _safe_write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    # write to named temp file then replace atomically
    with tempfile.NamedTemporaryFile('w', delete=False, dir=str(path.parent), encoding='utf-8') as tf:
        json.dump(obj, tf, ensure_ascii=False, indent=2)
        tempname = Path(tf.name)
    tempname.replace(path)

def load_user_data():
    if not USERS_FILE.exists():
        return {'farmers': [], 'buyers': []}
    with USERS_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    # ensure keys
    data.setdefault('farmers', [])
    data.setdefault('buyers', [])
    return data

def save_user_data(data):
    # Merge top-level keys conservatively
    existing = load_user_data()
    existing.update(data)
    _safe_write(USERS_FILE, existing)

def load_order_data():
    if not ORDERS_FILE.exists():
        return {'orders': []}
    with ORDERS_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)
    data.setdefault('orders', [])
    return data

def save_order_data(data):
    existing = load_order_data()
    existing.update(data)
    _safe_write(ORDERS_FILE, existing)

# compatibility wrappers
def load_orders():
    return load_order_data()

def save_orders(data):
    return save_order_data(data)
