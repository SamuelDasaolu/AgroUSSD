from src.interfaces.ussd_menu import USSDMenu
from src.interfaces.farmer_menu import farmer_menu
from src.interfaces.buyer_menu import buyer_menu
from src.interfaces.session_manager import SessionManager

def main():
    session = SessionManager()

    # === Registration / Login ===
    print("Welcome to AgroUSSD")
    role_choice = input("Select role:\n1. Farmer\n2. Buyer\nChoice: ")
    role = "farmer" if role_choice == "1" else "buyer"

    action = input("1. Register\n2. Login\nChoice: ")
    if action == "1":
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        pin = input("Set PIN: ")
        if not session.register_user(role, name, phone, pin):
            return
    else:
        phone = input("Enter phone number: ")
        pin = input("Enter PIN: ")
        if not session.login_user(role, phone, pin):
            return

    # === Launch menu ===
    if session.role == "farmer":
        current_menu = farmer_menu(session.active_user)
    else:
        current_menu = buyer_menu(session.active_user)

    while True:
        print("\n" + current_menu.display())
        choice = input("Enter choice: ")
        next_menu = current_menu.handle_input(choice)
        if next_menu is None:
            break
        current_menu = next_menu

if __name__ == "__main__":
    main()
