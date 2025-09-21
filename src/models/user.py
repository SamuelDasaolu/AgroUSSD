"""User Class in a USSD Workflow
Purpose

Represents the customer interacting with the USSD system.

Stores user-specific data such as phone number, session state, and selected inputs.

Acts as the "actor" that initiates and responds to USSD requests."""
from abc import ABC, abstractmethod
from src.utils import data_handler as dh
from src.utils.security import hash_pin, verify_pin

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

class User(ABC):
    role_key = None  # must be overridden by subclasses
    id_prefix = None  # must also be defined in subclasses

    def __init__(self, name, phone_number, pin):
        self.user_id = None  # generated automatically during registration
        self.name = name
        self.phone_number = phone_number
        self.__pin = pin  # store raw pin until registration
        self.is_authenticated = False

    def register(self):
        """Creates a user record in db"""
        users_data = dh.load_user_data()
        # Guard: subclass must define role_key and id_prefix
        if not self.role_key or not self.id_prefix:
            return False

        # Check DB if user already exists
        for user in users_data[self.role_key]:
            if user["phone_number"] == self.phone_number:
                return False

        # Generate unique ID (F### or B###)
        next_id = len(users_data[self.role_key]) + 1
        self.user_id = f"{self.id_prefix}{str(next_id).zfill(3)}"
        # Hash the pin for secure storage
        pin_meta = hash_pin(self.__pin)


        # Safety: avoid accidental duplicate user_id
        existing_ids = {u.get("user_id") for u in users_data.get(self.role_key, [])}
        if self.user_id in existing_ids:
            return False

        # user record for db
        user_record = {
            "user_id": self.user_id,
            "name": self.name,
            "phone_number": self.phone_number,
            "pin_meta": pin_meta
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
        self.last_message = message
        return True

    def authenticate(self, pin):
        if not self.role_key:
            return False

        users_data = dh.load_user_data()
        role_key = self.role_key

        # Find user in db by phone_number
        for user in users_data.get(role_key, []):
            if user.get("phone_number") == self.phone_number:
                # verify pin metadata
                pin_meta = user.get("pin_meta")
                if pin_meta and verify_pin(pin_meta, pin):
                    # Sync object attributes from DB
                    self.user_id = user.get("user_id")
                    self.name = user.get("name")
                    self.is_authenticated = True
                    return True
                else:
                    return False
        return False



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


# Re-export common concrete classes for convenience (tests expect these names here)
try:
    from src.models.farmer import Farmer
    from src.models.buyer import Buyer
except Exception:
    # import errors during test collection should not crash module import
    Farmer = None
    Buyer = None
