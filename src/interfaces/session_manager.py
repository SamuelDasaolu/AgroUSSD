from src.models.farmer import Farmer
from src.models.buyer import Buyer
from src.utils import data_handler as dh
import time, secrets
from typing import Dict, Any

class SessionManager:
    """Session manager with dual API:
    - Legacy simple API: register_user(role, name, phone, pin), login_user(role, phone, pin), logout(), active_user, role
    - Token API: create(user) -> token, get(token) -> session dict, destroy(token)
    """
    def __init__(self, timeout_seconds: int = 1800):
        self.active_user = None  # will hold a Farmer or Buyer instance
        self.role = None         # "farmer" or "buyer"
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self.timeout = timeout_seconds

    # ----- Legacy simple API used by CLI/main.py -----
    def register_user(self, role: str, name: str, phone: str, pin: str) -> bool:
        if role == "farmer":
            user = Farmer(name, phone, pin)
        else:
            user = Buyer(name, phone, pin)
        if user.register():
            self.active_user = user
            self.role = role
            return True
        return False

    def login_user(self, role: str, phone: str, pin: str) -> bool:
        if role == "farmer":
            user = Farmer("", phone, pin)
        else:
            user = Buyer("", phone, pin)
        if user.authenticate(pin):
            self.active_user = user
            self.role = role
            return True
        return False

    def logout(self):
        if self.active_user:
            self.active_user.logout()
        self.active_user = None
        self.role = None

    # ----- Token-based API for other callers -----
    def create(self, user_obj) -> str:
        """Create a session token for a user object (Farmer or Buyer). Returns token string."""
        token = secrets.token_hex(16)
        self._sessions[token] = {'user': user_obj, 'role': getattr(user_obj, 'role_key', None), 'ts': time.time()}
        return token

    def get(self, token: str):
        sess = self._sessions.get(token)
        if not sess:
            return None
        # expire check
        if time.time() - sess['ts'] > self.timeout:
            self._sessions.pop(token, None)
            return None
        # refresh timestamp
        sess['ts'] = time.time()
        return sess

    def destroy(self, token: str):
        self._sessions.pop(token, None)

    def cleanup(self):
        now = time.time()
        expired = [k for k,v in self._sessions.items() if now - v['ts'] > self.timeout]
        for k in expired:
            self._sessions.pop(k, None)
