"""User Class in a USSD Workflow
Purpose

Represents the customer interacting with the USSD system.

Stores user-specific data such as phone number, session state, and selected inputs.

Acts as the "actor" that initiates and responds to USSD requests."""
import hashlib
from abc import ABC, abstractmethod
from src.utils import data_handler as dh

# data/users.json SKELETON
users = {
    'farmers': [{
        'user_id': '',
        'name': '',
        'phone_number': '',
        'pin': '',
        'product': {

        },
        'market_id': ''
    },  # farmers stored as a list of dictionaries
    ],

    'buyers': [{
        'user_id': '',
        'name': '',
        'phone_number': '',
        'pin': '',
    },  # buyers also a list of dictionaries
    ]
}
# data/orders.json skeleton
orders = {
    "orders": [
        {
            "order_id": "",  # unique ID for the order
            "buyer_id": "",  # reference to buyer user_id
            "farmer_id": "",  # reference to farmer user_id
            "product_name": "",  # product being ordered
            "quantity": 0,  # quantity ordered
            "price_per_unit": 0.0,  # price per unit (at order time)
            "total_price": 0.0,  # calculated = quantity * price_per_unit
            "status": "pending",  # pending | completed | cancelled
            "timestamp": ""  # order creation time
        }
    ]
}


# --- Helpers ---
def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


class User(ABC):
    role_key = None  # must be overridden by subclasses
    id_prefix = None  # must also be defined in subclasses

    def __init__(self, name, phone_number, pin):
        self.user_id = None  # generated automatically during registration
        self.name = name
        self.phone_number = phone_number
        self.__pin = _hash_pin(pin)  # store hashed pin only
        self.is_authenticated = False

    def register(self):
        """Creates a user record in db"""
        users_data = dh.load_user_data()
        # Guard: subclass must define role_key and id_prefix
        if not self.role_key or not self.id_prefix:
            return {"success": False, "message": "User subclass must define role_key and id_prefix."}

        # Check DB if user already exists
        for user in users_data[self.role_key]:
            if user["phone_number"] == self.phone_number:
                return {"success": False, "message": "Phone number already registered."}

        # Generate unique ID (F### or B###)
        next_id = len(users_data[self.role_key]) + 1
        self.user_id = f"{self.id_prefix}{str(next_id).zfill(3)}"

        # Safety: avoid accidental duplicate user_id
        existing_ids = {u.get("user_id") for u in users_data.get(self.role_key, [])}
        if self.user_id in existing_ids:
            return {"success": False, "message": "Duplicate user ID detected."}

        # user record for db
        user_record = {
            "user_id": self.user_id,
            "name": self.name,
            "phone_number": self.phone_number,
            "pin": self.__pin
        }
        #
        # # Add farmer-specific fields
        # if role_key == "farmers":
        #     user_record["product"] = {}
        #     user_record["market_id"] = ""

        # Subclass hook to add extra fields e.g farmer to add product, harvest, etc
        self._extend_user_record(user_record)

        users_data[self.role_key].append(user_record)
        dh.save_user_data(users_data)
        message = f"{self.__class__.__name__} '{self.name}' registered successfully with ID {self.user_id}."
        return {"success": True, "message": message}

    def authenticate(self, pin):
        if not self.role_key:
            return {"success": False, "message": "User subclass must define role_key."}

        users_data = dh.load_user_data()
        hashed_pin = _hash_pin(pin)
        role_key = self.role_key

        # Find user in db by phone_number
        for user in users_data.get(role_key, []):
            if user["phone_number"] == self.phone_number and user["pin"] == hashed_pin:
                # Sync object attributes from DB
                self.user_id = user["user_id"]
                self.name = user["name"]
                self.phone_number = user["phone_number"]
                self.__pin = user["pin"]

                self.is_authenticated = True
                message = f"{self.__class__.__name__} {self.name} authenticated successfully. User ID: {self.user_id}"
                return {'success': True, 'message': message}

        return {"success": False, "message": "Authentication failed. Wrong phone number or PIN."}

    def logout(self):
        self.is_authenticated = False
        return {"success": True, "message": f"{self.name} logged out."}

    @abstractmethod
    def _extend_user_record(self, record: dict):
        """Subclass must implement to add role-specific fields into the saved record."""
        pass

    @abstractmethod
    def role_action(self):
        """Each role (Farmer/Buyer) will define its own actions"""
        pass
