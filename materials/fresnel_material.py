

import sys
from pyglm import glm
import math
from materials.material import Material

from octree import Octree
from ray import Ray

# TODO : ajouter le calcul des coefficient de fresnel pour avoir le ratio refraction reflexion

class FresnelMaterial(Material):
    obj = None
    refract_index = 1.0

    def __init__(self, refract_index = 1.0, color=glm.vec3(0.0,1.0,1.0)):
        super().__init__()
        self.color = glm.vec3(color)
        self.refract_index = refract_index

    def computeColor(self, hitPoint, ray, depth):
        super().computeColor(hitPoint, ray, depth)
        from scene import max_depth, list_of_objects, direction_light
        normal = self.obj.getNormal(hitPoint)
        entering = glm.dot(glm.normalize(ray.dir), normal) < 0
        n0 = 0
        n1 = 0
        eps = 1e-5
        color = glm.vec3(0.0,0.0,0.0)
        if self.refract_index != 0:
            if entering:
                n1_over_n2 = 1.0/self.refract_index
                n0 = 1.0
                n1 = self.refract_index
                offset_normal = -normal
            else:
                n1_over_n2 = self.refract_index/1.0
                n0 = self.refract_index
                n1 = 1.0
                normal = -normal
                offset_normal = -normal
        if depth <= max_depth:
            # compute the schlick approximation
            if self.refract_index == 0:
                refracted_valid = False
            else:
                R0 = ((n0-n1) / (n0 + n1)) * ((n0-n1) / (n0 + n1))
                Rt = 0
                Rt = R0 + (1-R0)*(1-(abs(glm.dot(glm.normalize(ray.dir),normal))))**5
                refract_dir = glm.refract(glm.normalize(ray.dir), normal, n1_over_n2)
                refracted_valid = not(abs(refract_dir[0]) < sys.float_info.epsilon and abs(refract_dir[1]) < sys.float_info.epsilon and abs(refract_dir[2]) < sys.float_info.epsilon)
            if not refracted_valid:
                Rt = 1.0
            if refracted_valid:
                refracted_ray = Ray(hitPoint + offset_normal * 0.00001, glm.normalize(refract_dir))
            reflected_dir = glm.reflect(glm.normalize(ray.dir), normal)
            reflected_ray = Ray(hitPoint, glm.normalize(reflected_dir))
            #print(hitPoint , hitPoint+R)
            min_t_refr = sys.float_info.max
            min_obj_refr = None
            min_t_ref = sys.float_info.max
            min_obj_ref = None
            hit_ref = None
            hit_refr = None
            for obj in list_of_objects:
                if refracted_valid:
                    hit_refr, obj_refr = obj.hit(refracted_ray)
                    if hit_refr is not None and hit_refr > eps and hit_refr < min_t_refr:
                        min_t_refr = hit_refr
                        min_obj_refr = obj_refr

                hit_ref, obj_ref = obj.hit(reflected_ray)
                if hit_ref is not None and hit_ref > eps and hit_ref < min_t_ref:
                    min_t_ref = hit_ref
                    min_obj_ref = obj_ref

            # accumulation des couleurs
            if min_obj_refr is not None and refracted_valid:
                p = refracted_ray.ray_cast(min_t_refr)
                c = min_obj_refr.getColor(p, refracted_ray, depth + 1)
                if c is not None:
                    color += (1.0 - Rt) * self.color * c

            if min_obj_ref is not None and Rt > sys.float_info.epsilon:
                p = reflected_ray.ray_cast(min_t_ref)
                c = min_obj_ref.getColor(p, reflected_ray, depth + 1)
                if c is not None:
                    color += Rt * self.color * c

            return color
        return None




        