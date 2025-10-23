from abc import ABC, abstractmethod
from ray import Ray

class Material(ABC):
    color = None

    @abstractmethod
    def computeColor(self, hitPoint, ray, depth):
        pass
    