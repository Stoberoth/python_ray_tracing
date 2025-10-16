from abc import ABC, abstractmethod

class Object(ABC):
    @abstractmethod
    def hit(self):
        pass
    