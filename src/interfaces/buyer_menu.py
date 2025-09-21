from src.interfaces.ussd_menu import USSDMenu
from src.utils import data_handler as dh
from src.utils.validators import is_positive_int

def _browse_action():
    def inner():
        data = dh.load_user_data()
        print("Available produce across farmers:")
        for farmer in data.get("farmers", []):
            products = farmer.get("product", {}) or farmer.get("products", {})
            if not products:
                continue
            for crop, qty in products.items():
                print(f"Farmer {farmer.get('user_id')} - {farmer.get('name')}: {crop} - {qty} units (phone: {farmer.get('phone_number')})")
        return None
    return inner

def _place_order_action(buyer):
    def inner():
        farmer_id = input("Enter farmer ID to buy from (e.g. F001): ").strip()
        product = input("Enter product name: ").strip()
        qty = input("Enter quantity: ").strip()
        if not is_positive_int(qty):
            print("Invalid quantity.")
            return None
        order = buyer.place_order(farmer_id, product, int(qty))
        if order:
            print(f"Order placed successfully. Order ID: {order.get('order_id')}")
        else:
            print("Order could not be placed. Check farmer ID, product availability, and quantity.")
        return None
    return inner

def _view_orders_action(buyer):
    def inner():
        orders = buyer.view_orders()
        if not orders:
            print("You have no orders.")
            return None
        print("Your orders:")
        for o in orders:
            print(f"- {o['quantity']} {o['product']} from Farmer {o['farmer_id']} on {o['timestamp']}")
        return None
    return inner

def buyer_menu(buyer):
    return USSDMenu(
        f"Buyer Menu - {buyer.name}",
        {
            "1": ("Browse Produce", _browse_action()),
            "2": ("Place Order", _place_order_action(buyer)),
            "3": ("View My Orders", _view_orders_action(buyer)),
        }
    )
