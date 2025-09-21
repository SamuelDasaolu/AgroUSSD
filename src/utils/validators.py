# src/utils/validators.py
import re

def is_valid_phone(phone: str) -> bool:
    """Check if the phone number is a basic Nigerian format (starts with +234 or 0 and has 11 digits)."""
    if not isinstance(phone, str):
        return False
    return bool(re.match(r"^(?:\+234|0)\d{10}$", phone))

def is_valid_pin(pin: str) -> bool:
    """Check if a PIN is 4–6 digits."""
    if not isinstance(pin, str):
        return False
    return bool(re.match(r"^\d{4,6}$", pin))

def is_positive_int(value) -> bool:
    """Check if value can be safely cast to a positive integer."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False
