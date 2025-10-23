from pyglm import glm
from materials.material import Material
import numpy as np
from ray import Ray


class BasicMaterial(Material):
    obj = None
    def __init__(self, color = [0.0,0.0,0.0]):
        super().__init__()
        self.color = color

    def computeColor(self, hitPoint, ray, depth):
        from scene import direction_light, list_of_objects
        super().computeColor(hitPoint, ray, depth)
        if direction_light.is_in_shadow(hitPoint, self.obj):
            return np.array([0,0,0])
        return np.array(self.color) * glm.dot(glm.normalize(direction_light.position - hitPoint), self.obj.getNormal(hitPoint))

