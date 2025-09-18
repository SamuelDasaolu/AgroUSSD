from src.interfaces.ussd_menu import USSDMenu
from src.models.farmer import Farmer

def add_produce(farmer: Farmer):
    crop = input("Enter crop name: ")
    qty = int(input("Enter quantity: "))
    if farmer.add_produce(crop, qty): print(f"{qty} units of {crop} added successfully!")


def view_produce(farmer: Farmer):
    produce = farmer.view_produce()  # fetch from DB
    if not produce:
        print("No produce registered yet.")
        return

    print(f"\n{farmer.name}'s Produce:")
    for crop, qty in produce.items():
        print(f"- {crop}: {qty} units")


def farmer_menu(farmer: Farmer):
    return USSDMenu(
        "Farmer Menu",
        {
            "1": ("Add Produce", lambda: add_produce(farmer)),
            "2": ("View Produce", lambda: view_produce(farmer)),
        }
    )
