import uuid
from datetime import datetime
from src.models.user import User
from src.utils import data_handler as dh


# Buyer Class
class Buyer(User):
    role_key = "buyers"
    id_prefix = "B"

    def __init__(self, name, phone_number, password):
        super().__init__(name, phone_number, password)
        self.orders = []

    def _extend_user_record(self, record: dict):
        # buyers currently have no extra fields; hook present for future extension
        pass

    def place_order(self, farmer_id, product_name, quantity):
        """Deduct stock from farmer when buyer places an order"""
        data = dh.load_user_data()
        for farmer in data["farmers"]:
            if farmer["user_id"] == farmer_id:
                if product_name not in farmer["product"]:
                    print("Product not available.")
                    return Falselse
                if farmer["product"][product_name] < quantity:
                    print("Not enough stock available.")
                    return Falselse

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
                orders_data.setdefault("orders", [])
                orders_data["orders"].append(new_order)
                dh.save_order_data(orders_data)
                print(f"Order placed: {quantity} units of {product_name} from Farmer {farmer['name']}.")
                return new_order
        print("Farmer not found.")
        return Falselse

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
