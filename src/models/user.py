"""User Class in a USSD Workflow
Purpose

Represents the customer interacting with the USSD system.

Stores user-specific data such as phone number, session state, and selected inputs.

Acts as the "actor" that initiates and responds to USSD requests."""


from abc import ABC, abstractmethod
from pathlib import Path
from ..utils import data_handler as dh

# # Abstract User Class
# save_folder = Path("data").mkdir(exist_ok=True)
# filepath = save_folder/'users.json'
# # USERS.json skeleton
users = {
    'farmers': {
        'user_id': '',
        'name': '',
        'phone_number': '',
        'pin': '',
        'product' : {
            
        },
        'market_id' : ''
    },

    'buyers': {
        'user_id': '',
        'name': '',
        'phone_number': '',
        'pin': '',
    },
}
# DATA SKELETON

class User(ABC):
    def __init__(self, user_id, name, phone_number, pin):
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number
        self.__pin = pin  # private
        self.is_authenticated = False

    def register(self, type):
        # Creates a user record in db
        user_data = dh.load_user_data()
        user_record = {
        "user_id": self.user_id,
        "name": self.name,
        "phone_number": self.phone_number,
        "pin": self.pin
        }
        for farmer, buyer in (user_data['farmers'], user_data['buyers']):
            if self.user_id in farmer.values() or self.user_id in buyer.values():
                print('User has been registered before. Try resetting pin in profile')
            else: dh.save_user_data(user_record)
        print(
            f"{self.__class__.__name__} '{self.name}' registered with phone {self.phone_number}")

    def authenticate(self, pin):
        if self.__pin == pin:
            self.is_authenticated = True
            print(f"{self.name} authenticated successfully.")
            return True
        else:
            print("Authentication failed. Wrong password.")
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
    def __init__(self, user_id, name, phone_number, pin):
        super().__init__(user_id, name, phone_number, pin)
        self.produce_list = []

    def add_produce(self, item):
        self.produce_list.append(item)
        print(f"{self.name} added produce: {item}")

    def view_produce(self):
        print(f"{self.name}'s produce list: {self.produce_list}")
        return self.produce_list

    def role_action(self):
        print(f"Farmer {self.name} can add and view produce.")


# Buyer Class
class Buyer(User):
    def __init__(self, user_id, name, phone_number, password):
        super().__init__(user_id, name, phone_number, password)
        self.orders = []

    def place_order(self, item):
        self.orders.append(item)
        print(f"{self.name} placed an order for: {item}")

    def view_orders(self):
        print(f"{self.name}'s orders: {self.orders}")
        return self.orders

    def role_action(self):
        print(f"Buyer {self.name} can place and view orders.")


# Register Farmer
farmer = Farmer(user_id=1, name="John",
                phone_number="+2348012345678", password="1234")
farmer.register()

# Authenticate Farmer
farmer.authenticate("1234")
farmer.add_produce("Tomatoes")
farmer.view_produce()

# Register Buyer
buyer = Buyer(user_id=2, name="Mary",
              phone_number="+2348098765432", password="5678")
buyer.register()

# Authenticate Buyer
buyer.authenticate("5678")
buyer.place_order("Tomatoes")
buyer.view_orders()

# Logout users
farmer.logout()
buyer.logout()
