# main.py
from buyer_menu import buyer_menu
from farmer_menu import farmer_menu

class Buyer:
    def __init__(self, ussd):
        self.ussd = ussd
    
    def display_menu(self):
        buyer_menu(self.ussd)

class Farmer:
    def __init__(self, ussd):
        self.ussd = ussd
    
    def display_menu(self):
        farmer_menu(self.ussd)

class MainMenu:
    def __init__(self):
        self.ussd = None  # You can initialize with actual USSD data if needed
    
    def display_main_menu(self):
        while True:
            print("\n....Main Menu.... ")
            print("1. Buyer")
            print("2. Farmer")
            print("3. Exit")
            choice = input("Select an option: ")
            
            if choice == "1":
                buyer = Buyer(self.ussd)
                buyer.display_menu()
            elif choice == "2":
                farmer = Farmer(self.ussd)
                farmer.display_menu()
            elif choice == "3":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    api = MainMenu()
    api.display_main_menu()
