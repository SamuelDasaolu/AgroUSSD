# src/utils/validators.py
import re

def is_valid_phone(value: str) -> bool:
    """Basic phone check: digits only, reasonable length (7-15)."""
    if not isinstance(value, str):
        return False
    return value.isdigit() and 7 <= len(value) <= 15

def is_valid_pin(value: str) -> bool:
    """Check if a PIN is 4–6 digits."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r"^\d{4,6}$", value))

def is_positive_int(value) -> bool:
    """Check if value can be safely cast to a positive integer (> 0)."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False
