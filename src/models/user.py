from abc import ABC, abstractmethod

# Base class for farmer and buyer
class User(ABC):
    def __init__(self, name, phone):
        self.name = name
        self.name = phone

    @abstractmethod
    def get_role(self) -> str:
        pass