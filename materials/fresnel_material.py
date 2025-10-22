

import sys
from pyglm import glm
import math
from materials.material import Material

from ray import Ray


class FresnelMaterial(Material):
    obj = None
    refract_index = 1.0

    def __init__(self, refract_index = 1.0, color=[0.0,1.0,1.0]):
        super().__init__()
        self.color = color
        self.refract_index = refract_index

    def shadowing(self, lightPos, point, objects, current_obj):
        return super().shadowing(lightPos, point, objects, current_obj)

    def computeColor(self, hitPoint, ray, depth):
        super().computeColor(hitPoint, ray, depth)
        from scene import max_depth, list_of_objects, direction_light
        normal = self.obj.getNormal(hitPoint)
        entering = glm.dot(ray.dir, normal) < 0
        if entering:
            n1_over_n2 = 1.0/self.refract_index
            offset_normal = -normal
        else:
            n1_over_n2 = self.refract_index/1.0
            normal = -normal
            offset_normal = -normal
        if depth <= max_depth:
            hit, hits = self.obj.hit(ray)       
            #k = 1.0 - 1.0*(1.0 - glm.dot(self.obj.getNormal(hitPoint), ray.dir) * glm.dot(self.obj.getNormal(hitPoint), ray.dir))
            #R = 1.0 * ray.dir - (1.0 * glm.dot(self.obj.getNormal(hitPoint), ray.dir + math.sqrt(k)) * self.obj.getNormal(hitPoint))
            R = glm.refract(ray.dir, normal, n1_over_n2)
            #if refracted_dir[0] < sys.float_info.epsilon and refracted_dir[1] < sys.float_info.epsilon and refracted_dir[2] < sys.float_info.epsilon:
            #    return None
            refracted_ray = Ray(hitPoint + offset_normal * 0.00001, R)
            #print(hitPoint , hitPoint+R)
            min = sys.float_info.max
            minObj = None
            for object in list_of_objects:
                hit, hits = object.hit(refracted_ray)
                if hit != None and min > hit:
                    min = hit
                    minObj = object
            if minObj != None:
                p = refracted_ray.ray_cast(min)
                #color = self.color * minObj.getColor(direction_light,p, self, refracted_ray, depth +1)
                color = self.color * minObj.getColor(direction_light,p, self, refracted_ray, depth +1)
                return color
        return None




        