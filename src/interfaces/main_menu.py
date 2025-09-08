def main_menu():
 menu = input("Do you have an account: Yes/No").strip().lower()
 if menu != "yes":
   print()
   menu_2 = input("Select the number of any of the following\n1. Farmer Menu\n2. Buyer Menu\n3. Exit").strip()
 if menu_2 == "1":
   farmer_choice = input("Are you a farmer: Yes/No").strip().lower()
   if farmer_choice != "yes":
     print("If you're not a farmer, select buyer or exit")
   elif farmer_choice == "no":
    
    


def user_registration():
  