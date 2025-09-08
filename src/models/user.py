"""User Class in a USSD Workflow
Purpose

Represents the customer interacting with the USSD system.

Stores user-specific data such as phone number, session state, and selected inputs.

Acts as the "actor" that initiates and responds to USSD requests."""
import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from src.utils import data_handler as dh

# data/users.json SKELETON
users = {
    'farmers': [{
        'user_id': '',
        'name': '',
        'phone_number': '',
        'pin': '',
        'product': {

        },  # Change to list later on
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
            "order_id": "",        # unique ID for the order
            "buyer_id": "",        # reference to buyer user_id
            "farmer_id": "",       # reference to farmer user_id
            "product_name": "",    # product being ordered
            "quantity": 0,         # quantity ordered
            "price_per_unit": 0.0, # price per unit (at order time)
            "total_price": 0.0,    # calculated = quantity * price_per_unit
            "status": "pending",   # pending | completed | cancelled
            "timestamp": ""        # order creation time
        }
    ]
}


class User(ABC):
    def __init__(self, name, phone_number, pin):
        self.user_id = None  # generated automatically during registration
        self.name = name
        self.phone_number = phone_number
        self.__pin = pin  # private
        self.is_authenticated = False

    def register(self):
        """Creates a user record in db"""
        users_data = dh.load_user_data()

        # Check if user already exists
        role_key = "farmers" if isinstance(self, Farmer) else "buyers"
        for user in users_data[role_key]:
            if user["phone_number"] == self.phone_number:
                print(f"Registration failed: {self.phone_number} already registered.")
                return False

        # Generate unique ID (F### or B###)
        prefix = "F" if isinstance(self, Farmer) else "B"
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
        if isinstance(self, Farmer):
            user_record["product"] = {}
            user_record["market_id"] = ""

        users_data[role_key].append(user_record)
        dh.save_user_data(users_data)
        print(f"{self.__class__.__name__} '{self.name}' registered successfully with ID {self.user_id}.")
        return True

    def authenticate(self, pin):
        users_data = dh.load_user_data()
        role_key = "farmers" if isinstance(self, Farmer) else "buyers"

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


# Farmer Class
class Farmer(User):
    def __init__(self, name, phone_number, pin):
        super().__init__(name, phone_number, pin)

    def add_produce(self, product_name, quantity):
        data = dh.load_user_data()
        for farmer in data['farmers']:
            if farmer['user_id'] == self.user_id:
                farmer['product'][product_name] = farmer['product'].get(product_name, 0) + quantity
                dh.save_user_data(data)
                print(f"Added {quantity} units of {product_name}.")
                print(f"Current Stock:  {farmer['product'][product_name]} units.")
                return True
        print("Farmer doesn't exist in our database")
        return False

    def view_produce(self):
        data = dh.load_user_data()
        for farmer in data["farmers"]:
            if farmer["user_id"] == self.user_id:
                print(f"{self.name}'s produce: {farmer['product']}")
                return farmer["product"]
        return {}

    def view_orders(self):
        orders_data = dh.load_order_data()
        my_orders = [order for order in orders_data.get('orders', []) if order["farmer_id"] == self.user_id]

        if not my_orders:
            print(f"No orders found for Farmer {self.name}.")
            return []

        print(f"Orders for Farmer {self.name}:")
        for o in my_orders:
            print(f"- {o['quantity']} {o['product']} ordered by Buyer {o['buyer_id']} on {o['timestamp']}")
        return my_orders

    def role_action(self):
        print(f"Farmer {self.name} can add and view produce.")


# Buyer Class
class Buyer(User):
    def __init__(self, name, phone_number, password):
        super().__init__(name, phone_number, password)
        self.orders = []

    def place_order(self, farmer_id, product_name, quantity):
        """Deduct stock from farmer when buyer places an order"""
        data = dh.load_user_data()
        for farmer in data["farmers"]:
            if farmer["user_id"] == farmer_id:
                if product_name not in farmer["product"]:
                    print("Product not available.")
                    return False
                if farmer["product"][product_name] < quantity:
                    print("Not enough stock available.")
                    return False

                # Deduct stock
                farmer["product"][product_name] -= quantity
                if farmer["product"][product_name] == 0:
                    del farmer["product"][product_name]  # remove product if depleted

                dh.save_user_data(data)

                orders_data = dh.load_order_data()
                new_order = {
                    "order_id": str(uuid.uuid4()),
                    "buyer_id": self.user_id,
                    "farmer_id": farmer_id,
                    "product": product_name,
                    "quantity": quantity,
                    "timestamp": datetime.now().isoformat()
                }
                orders_data["orders"].append(new_order)
                dh.save_order_data(orders_data)
                print(f"Order placed: {quantity} units of {product_name} from Farmer {farmer['name']}.")
                return True
        print("Farmer not found.")
        return False

    def view_orders(self):
        orders_data = dh.load_order_data()
        my_orders = [order for order in orders_data.get("orders", []) if order["buyer_id"] == self.user_id]

        if not my_orders:
            print(f"No orders found for {self.name}.")
            return []

        print(f"Orders for {self.name}:")
        for o in my_orders:
            print(f"- {o['quantity']} {o['product']} from Farmer {o['farmer_id']} on {o['timestamp']}")
        return my_orders

    def role_action(self):
        print(f"Buyer {self.name} can place and view orders.")


# Register Farmer
farmer = Farmer("Adamu", "+456546", "1234")
# farmer.register()
farmer.authenticate("1234")
# farmer.add_produce("Corn", 100)
# Register Buyer
buyer = Buyer("Kemi", "+32443545", "5678")
# buyer.register()
buyer.authenticate("5678")

# Buyer places an order
buyer.place_order(farmer.user_id, "Tomatoes", 20)

# Farmer checks his orders
farmer.view_orders()

# Buyer checks her orders
buyer.view_orders()

# Logout users
farmer.logout()
buyer.logout()
