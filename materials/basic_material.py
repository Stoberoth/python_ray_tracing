from pyglm import glm
from materials.material import Material
import numpy as np


class BasicMaterial(Material):
    obj = None
    def __init__(self, color = [0.0,0.0,0.0]):
        super().__init__()
        self.color = color

    def computeColor(self, hitPoint, ray):
        from scene import direction_light
        super().computeColor(hitPoint, ray)
        return np.array(self.color) * glm.dot(glm.normalize(direction_light.position - hitPoint), self.obj.getNormal(hitPoint))

