from abc import ABC, abstractmethod
import ray

class Object(ABC):
    @abstractmethod
    def hit(self, r : ray.Ray):
        pass
    