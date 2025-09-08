from user import User
from random import randint
class Buyer(User):
    def __init__(self, name: str, phone: str, interest):
        super().__init__(name, phone)
        self.interest = interest
        self.unique_id = f"BYR {randint(1000, 9999)}"

    def get_role(self) -> str:
        return "Buyer"