from src.models.farmer import Farmer
from src.models.buyer import Buyer
from src.utils import data_handler as dh

class SessionManager:
    def __init__(self):
        self.active_user = None  # will hold a Farmer or Buyer instance
        self.role = None         # "farmer" or "buyer"

    def register_user(self, role, name, phone, pin):
        if role == "farmer":
            user = Farmer(name, phone, pin)
        else:
            user = Buyer(name, phone, pin)
        if user.register():
            self.active_user = user
            self.role = role
            return True
        return False

    def login_user(self, role, phone, pin):
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
