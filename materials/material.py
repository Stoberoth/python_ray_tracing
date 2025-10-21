from abc import ABC, abstractmethod
from ray import Ray

class Material(ABC):
    color = None

    @abstractmethod
    def computeColor(self, hitPoint, ray, depth):
        pass

    @abstractmethod
    def shadowing(self, lightPos, point, objects, current_obj):
        ray_dir = point - lightPos
        r = Ray(lightPos, ray_dir)
        for o in objects:
            t = o.hit(r)
            if t == None or current_obj == o:
                continue
            elif t > 0 and t < 1:
                return True
        return False
    