from src.models.user import User
from src.utils import data_handler as dh


# Farmer Class
class Farmer(User):
    role = "farmers"

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
