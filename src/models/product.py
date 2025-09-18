from abc import ABC, abstractmethod

# Base class for crops, livestock and processed goods
class Product(ABC):
    def __init__(self, name: str, price: int, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def get_info(self, price: int) -> str:
        pass