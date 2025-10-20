from abc import ABC, abstractmethod

class Material(ABC):
    color = None

    @abstractmethod
    def computeColor(self, hitPoint, ray):
        pass
    