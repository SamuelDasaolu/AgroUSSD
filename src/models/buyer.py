import uuid
from datetime import datetime
from src.models.user import User
from src.utils import data_handler as dh

class Buyer(User):
    role_key = 'buyers'
    id_prefix = 'B'

    def __init__(self, name: str, phone_number: str, pin: str):
        super().__init__(name, phone_number, pin)

    def _extend_user_record(self, record: dict):
        record.setdefault('orders', [])

    def place_order(self, farmer_id: str, product_name: str, quantity: int):
        data = dh.load_user_data()
        # find farmer
        for f in data.get('farmers', []):
            if f.get('user_id') == farmer_id:
                products = f.setdefault('product', {})
                if product_name not in products:
                    return None
                if products[product_name] < int(quantity):
                    return None
                # deduct stock
                products[product_name] -= int(quantity)
                if products[product_name] == 0:
                    del products[product_name]
                dh.save_user_data(data)
                # create order
                orders = dh.load_order_data()
                order_id = str(uuid.uuid4())
                order = {
                    'order_id': order_id,
                    'farmer_id': farmer_id,
                    'buyer_id': self.user_id,
                    'product': product_name,
                    'quantity': int(quantity),
                    'timestamp': datetime.utcnow().isoformat()
                }
                orders.setdefault('orders', []).append(order)
                dh.save_order_data(orders)
                return order
        return None

    def view_orders(self):
        orders = dh.load_order_data()
        return [o for o in orders.get('orders', []) if o.get('buyer_id') == self.user_id]

    def role_action(self):
        print(f"Buyer {self.name} can place and view orders.")
