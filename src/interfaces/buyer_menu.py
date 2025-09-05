# buyer_menu.py

def buyer_menu(ussd):
    print("\n Buyer Menu")
    print("1. Authentication")
    print("2. View Available Produce")
    print("3. Search by Crop")
    print("4. Back")
    choice = input("Select an option: ")

    if choice == "1":
        print("Authentication") # pending the time to add Authenticcation function
    elif choice == "2":
        print("Available produce") # pending the time to add available produce function
    elif choice == "3":
        print("Search by crop") # pending the time to add search crop function
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
