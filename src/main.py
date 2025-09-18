from src.models.buyer import Buyer
from src.models.farmer import Farmer

# Register Farmer
farmer = Farmer("Adamu", "+456546", "1234")
# farmer.register()
farmer.authenticate("1234")
# farmer.add_produce("Corn", 100)
# Register Buyer
buyer = Buyer("Samuel", "+7233243", "5678")
buyer.register()
buyer.authenticate("5678")

# Buyer places an order
buyer.place_order(farmer.user_id, "Corn", 20)

# Farmer checks his orders
farmer.view_orders()

# Buyer checks her orders
buyer.view_orders()

# Logout users
farmer.logout()
buyer.logout()
