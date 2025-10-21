# material which will reflect the environment on it's surface
import sys
from types import NoneType
from pyglm import glm
import light
from materials.material import Material
import numpy as np

from ray import Ray

class ReflectiveMaterial(Material):
    obj = None

    def shadowing(self, lightPos, point, objects, current_obj):
        return super().shadowing(lightPos, point, objects, current_obj)

    def computeColor(self, hitPoint, ray, depth):
        from scene import list_of_objects, direction_light, camera, max_depth
        super().computeColor(hitPoint, ray, depth)
        if(depth < max_depth):
            reflect_dir = glm.reflect(ray.dir, self.obj.getNormal(hitPoint))
            r = Ray(hitPoint, reflect_dir)
            min = sys.float_info.max
            for object in list_of_objects:
                hit = object.hit(r)
                minObj = None
                if hit != None and min > hit and object != self.obj:
                    min = hit
                    minObj = object
                if minObj != None:
                    p = r.ray_cast(min)
                    #if type(minObj.getColor(light, p, self, r, depth+1)) != NoneType:
                    color = minObj.getColor(light, p, self, r, depth+1)
            return color
        return None
