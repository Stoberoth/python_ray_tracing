# material which will reflect the environment on it's surface
import sys
from pyglm import glm
import light
from materials.material import Material
from ray import Ray

class ReflectiveMaterial(Material):
    obj = None

    def computeColor(self, hitPoint, ray):
        from scene import list_of_objects, direction_light, camera
        super().computeColor(hitPoint, ray)
        reflect_dir = glm.reflect(ray.dir, self.obj.getNormal(hitPoint))
        r = Ray(hitPoint, reflect_dir)
        min = sys.float_info.max
        color = [0.0,0.0,0.0]
        for object in list_of_objects:
            hit = object.hit(r)
            minObj = None
            if hit != None and min > hit and object != self.obj:
                min = hit
                minObj = object
            if minObj != None:
                p = r.ray_cast(min)
                color = minObj.getColor(light, p, self, r)
        return color
