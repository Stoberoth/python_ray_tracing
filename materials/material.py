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
        from materials.fresnel_material import FresnelMaterial
        for o in objects:
            t, discriminant = o.hit(r)
            if t == None or current_obj == o:
                continue
            elif t > 0.0 and t < 1.0 and type(o.mat)!=FresnelMaterial:
                #return True
                return False
        return False
    