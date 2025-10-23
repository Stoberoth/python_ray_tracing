from pyglm import glm
from materials.fresnel_material import FresnelMaterial
from ray import Ray

class Light:
    position = glm.vec3(0.0,0.0,0.0)
    color = glm.vec3(1.0,1.0,1.0)

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def is_in_shadow(self, hitPoint, check_obj):
        from scene import list_of_objects
        from materials import fresnel_material
        # not normalize because I want to check if we arrive or not to the point we want
        light_ray = Ray(self.position, hitPoint - self.position)
        for obj in list_of_objects:
            t = obj.hit(light_ray)
            if t == None or check_obj == obj:
                continue
            elif t > 0.0 and t < 1.0 and type(obj.mat) != FresnelMaterial:
                return True
        return False

    def getPosition(self):
        return self.position
    
    def getColor(self):
        return self.color

    