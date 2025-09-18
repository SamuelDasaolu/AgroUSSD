from src.interfaces.ussd_menu import USSDMenu
from src.utils import data_handler as dh

def browse_produce():
    data = dh.load_user_data()
    print("Available produce:")
    for farmer in data["farmers"]:
        for crop, qty in farmer.get("product", {}).items():
            print(f"{crop}: {qty} units from Farmer {farmer.get('name', 'unknown')}")

def buyer_menu():
    return USSDMenu(
        "Buyer Menu",
        {
            "1": ("Browse Produce", browse_produce),
        }
    )
