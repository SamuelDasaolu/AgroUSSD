"""User Class in a USSD Workflow
Purpose

Represents the customer interacting with the USSD system.

Stores user-specific data such as phone number, session state, and selected inputs.

Acts as the "actor" that initiates and responds to USSD requests."""
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


class User(ABC):
    role = None  # must be overridden by subclasses

    def __init__(self, name, phone_number, pin):
        self.user_id = None  # generated automatically during registration
        self.name = name
        self.phone_number = phone_number
        self.__pin = pin  # private
        self.is_authenticated = False

    def register(self):
        """Creates a user record in db"""
        users_data = dh.load_user_data()
        # Check DB if user already exists
        if not self.role:
            raise ValueError("Subclasses of User must define a role.")

        role_key = self.role

        for user in users_data[role_key]:
            if user["phone_number"] == self.phone_number:
                print(f"Registration failed: {self.phone_number} already registered.")
                return False

        # Generate unique ID (F### or B###)
        prefix = "F" if role_key == "farmers" else "B"
        next_id = len(users_data[role_key]) + 1
        self.user_id = f"{prefix}{str(next_id).zfill(3)}"

        # user record for db
        user_record = {
            "user_id": self.user_id,
            "name": self.name,
            "phone_number": self.phone_number,
            "pin": self.__pin
        }

        # Add farmer-specific fields
        if role_key == "farmers":
            user_record["product"] = {}
            user_record["market_id"] = ""

        users_data[role_key].append(user_record)
        dh.save_user_data(users_data)
        print(f"{self.__class__.__name__} '{self.name}' registered successfully with ID {self.user_id}.")
        return True

    def authenticate(self, pin):
        users_data = dh.load_user_data()
        role_key = self.role

        # Find user in db by phone_number
        for user in users_data.get(role_key, []):
            if user["phone_number"] == self.phone_number and user["pin"] == pin:
                # Sync object attributes from DB
                self.user_id = user["user_id"]
                self.name = user["name"]
                self.phone_number = user["phone_number"]
                self.__pin = user["pin"]

                self.is_authenticated = True
                print(f"{self.name} authenticated successfully. User ID: {self.user_id}")
                return True

        print("Authentication failed. Wrong phone number or PIN.")
        return False

    def logout(self):
        self.is_authenticated = False
        print(f"{self.name} logged out.")

    @abstractmethod
    def role_action(self):
        """Each role (Farmer/Buyer) will define its own actions"""
        pass
