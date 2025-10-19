from abc import ABC, abstractmethod
import ray

class Object(ABC):
    @abstractmethod
    def hit(self, r : ray.Ray):
        pass

    @abstractmethod
    def getColor(self, light, hitPoint, camera):
        pass
    
    @abstractmethod
    def getNormal(self, point):
        pass