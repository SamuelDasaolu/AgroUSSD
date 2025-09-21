from abc import ABC, abstractmethod
from typing import Dict, Any
from src.utils import data_handler as dh
from src.utils.security import hash_pin, verify_pin

class User(ABC):
    role_key: str = None
    id_prefix: str = None

    def __init__(self, name: str, phone_number: str, pin: str):
        self.user_id = None
        self.name = name
        self.phone_number = phone_number
        self._pin = pin
        self.is_authenticated = False
        self.last_message = ''

    def register(self) -> bool:
        users = dh.load_user_data()
        if not getattr(self, 'role_key', None) or not getattr(self, 'id_prefix', None):
            return False
        users.setdefault(self.role_key, [])
        # check duplicate phone
        for u in users[self.role_key]:
            if u.get('phone_number') == self.phone_number:
                return False
        # assign id
        next_id = len(users[self.role_key]) + 1
        self.user_id = f"{self.id_prefix}{str(next_id).zfill(3)}"
        # hash pin
        pin_meta = hash_pin(self._pin)
        record = {
            'user_id': self.user_id,
            'name': self.name,
            'phone_number': self.phone_number,
            'pin_meta': pin_meta
        }
        # subclass hook
        self._extend_user_record(record)
        users[self.role_key].append(record)
        dh.save_user_data(users)
        self.last_message = f"{self.__class__.__name__} '{self.name}' registered successfully with ID {self.user_id}."
        return True

    def authenticate(self, pin: str) -> bool:
        users = dh.load_user_data()
        for u in users.get(self.role_key, []):
            if u.get('phone_number') == self.phone_number:
                pin_meta = u.get('pin_meta')
                if pin_meta and verify_pin(pin_meta, pin):
                    self.user_id = u.get('user_id')
                    self.name = u.get('name')
                    self.is_authenticated = True
                    return True
                return False
        return False

    def logout(self) -> bool:
        self.is_authenticated = False
        return True

    @abstractmethod
    def _extend_user_record(self, record: Dict[str, Any]):
        pass

    @abstractmethod
    def role_action(self):
        pass

# re-export concrete classes for tests that expect from src.models.user import Farmer, Buyer
try:
    from src.models.farmer import Farmer  # noqa: E402, F401
    from src.models.buyer import Buyer    # noqa: E402, F401
except Exception:
    Farmer = None
    Buyer = None
