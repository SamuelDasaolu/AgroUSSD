class Harvest:
    def __init__(self, farmer_id: str, crop_name: str, quantity: int):
        self.farmer_id = farmer_id
        self.crop_name = crop_name
        self.quantity = quantity

    def update_quantity(self, quantity_sold: int) -> bool:
        if quantity_sold <= self.quantity:
            self.quantity -= quantity_sold
            return True
        return False
    
    def get_harvest_info(self) -> str:
        return f"Product: {self.crop_name} | Quantity: {self.quantity} units"