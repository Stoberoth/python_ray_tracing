from abc import ABC, abstractmethod
import ray

class Object(ABC):
    mat = None
    parent = None
    @abstractmethod
    def hit(self, r : ray.Ray):
        pass

    @abstractmethod
    def getColor(self, hitPoint, depth):
        pass
    
    @abstractmethod
    def getNormal(self, point):
        pass