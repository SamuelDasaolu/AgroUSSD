# src/interfaces/farmer_menu.py
from src.interfaces.ussd_menu import USSDMenu
from src.utils.validators import is_positive_int

def _add_produce_action(farmer):
    def inner():
        crop = input("Enter crop name: ").strip()
        qty = input("Enter quantity: ").strip()
        if not is_positive_int(qty):
            print("Invalid quantity. Must be a positive integer.")
            return None
        success = farmer.add_produce(crop, int(qty))
        if success:
            print(f"Added {qty} units of {crop} to your inventory.")
        else:
            print("Failed to add produce. Make sure you're registered and try again.")
        return None
    return inner

def _view_produce_action(farmer):
    def inner():
        prod = farmer.view_produce()
        if not prod:
            print("No produce recorded yet.")
            return None
        print(f"Produce for {farmer.name}:")
        for k, v in prod.items():
            print(f"- {k}: {v} units")
        return None
    return inner

def _view_orders_action(farmer):
    def inner():
        orders = farmer.list_my_orders()
        if not orders:
            print("No orders for your farm yet.")
            return None
        print("Orders:")
        for o in orders:
            print(f"- {o['quantity']} {o['product']} for Buyer {o['buyer_id']} on {o['timestamp']}")
        return None
    return inner

def farmer_menu(farmer):
    return USSDMenu(
        f"Farmer Menu - {farmer.name}",
        {
            "1": ("Add Produce", _add_produce_action(farmer)),
            "2": ("View Produce", _view_produce_action(farmer)),
            "3": ("View Orders", _view_orders_action(farmer)),
        }
    )
