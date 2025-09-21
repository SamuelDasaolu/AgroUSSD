from src.models.user import User
from src.utils import data_handler as dh

class Farmer(User):
    role_key = 'farmers'
    id_prefix = 'F'

    def __init__(self, name: str, phone_number: str, pin: str):
        super().__init__(name, phone_number, pin)

    def _extend_user_record(self, record: dict):
        record.setdefault('product', {})  # product_name -> qty

    def add_produce(self, product_name: str, quantity: int) -> bool:
        data = dh.load_user_data()
        # find farmer by user_id if exists, else use temp user before register
        if not self.user_id:
            # try to find by phone
            for f in data.get('farmers', []):
                if f.get('phone_number') == self.phone_number:
                    self.user_id = f.get('user_id')
                    break

        # If farmer not registered, cannot add produce
        if not self.user_id:
            # allow adding to in-memory record then require register to persist
            # but for simplicity, require registration first
            return False

        for f in data.get('farmers', []):
            if f.get('user_id') == self.user_id:
                prod = f.setdefault('product', {})
                prod[product_name] = prod.get(product_name, 0) + int(quantity)
                dh.save_user_data(data)
                return True
        return False

    def view_produce(self):
        data = dh.load_user_data()
        for f in data.get('farmers', []):
            if f.get('phone_number') == self.phone_number or f.get('user_id') == self.user_id:
                return f.get('product', {})
        return {}

    def list_my_orders(self):
        orders = dh.load_order_data()
        return [o for o in orders.get('orders', []) if o.get('farmer_id') == self.user_id]

    def role_action(self):
        print(f"Farmer {self.name} can list and manage produce.")
