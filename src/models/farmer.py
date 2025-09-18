from user import User
from random import randint

class Farmer(User):
    def __init__(self, name: str, phone: str, farm_size: str, crop: list):
        super().__init__(name, phone)
        self.farm_size = farm_size
        self.crop = crop
        self.unique_id = f"FMR {randint(1000, 9999)}"

    def get_role(self) -> str:
        return "Farmer" 