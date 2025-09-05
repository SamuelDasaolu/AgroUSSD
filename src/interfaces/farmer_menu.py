# farmer_menu.py

def farmer_menu(ussd):
    print("\n Farmer Menu")
    print("1. Authentication")
    print("2. View Market Prices")
    print("3. List/Update Produce")
    print("4. Back")
    choice = input("Select an option: ")

    if choice == "1":
        print("AUTHENTICATION") # Probably going to add Authenticatin function 
    elif choice == "2":
        print("Market price")  # pending the time we will add market price function
    elif choice == "3":
        print("Update produce") # pending the time to add market price function
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
