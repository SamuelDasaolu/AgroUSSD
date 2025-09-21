import os, hashlib, hmac, base64
from typing import Dict, Any

def hash_pin(pin: str, salt: bytes = None, iterations: int = 200_000) -> Dict[str, Any]:
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', pin.encode('utf-8'), salt, iterations)
    return {
        "salt": base64.b64encode(salt).decode('ascii'),
        "hash": base64.b64encode(key).decode('ascii'),
        "iterations": iterations
    }

def verify_pin(stored: Dict[str, Any], candidate_pin: str) -> bool:
    try:
        salt = base64.b64decode(stored['salt'])
        iters = int(stored.get('iterations', 200_000))
        candidate_key = hashlib.pbkdf2_hmac('sha256', candidate_pin.encode('utf-8'), salt, iters)
        return hmac.compare_digest(base64.b64encode(candidate_key).decode('ascii'), stored['hash'])
    except Exception:
        return False
