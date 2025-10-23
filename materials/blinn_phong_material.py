from pyglm import glm

from materials.material import Material
import numpy as np
from ray import Ray

class BlinnPhongMaterial(Material):
    ambient_scale = 0.2
    specular_strength = 0.1
    specular_power = 32
    obj = None

    def __init__(self, ambient_scale = 0.2, specular_strength = 0.1, specular_power = 32, color= [0.5,0.5,0.5]) :
        super().__init__()
        self.ambient_scale = ambient_scale
        self.specular_strength = specular_strength
        self.specular_power = specular_power
        self.color = color

    def computeColor(self, hitPoint, ray, depth):
        from scene import direction_light, camera, list_of_objects
        super().computeColor(hitPoint, ray, depth)
        if direction_light.is_in_shadow(hitPoint, self.obj):
            return np.array([0,0,0])
        else:
            ambient = self.ambient_scale * direction_light.color

            light_dir = glm.normalize(direction_light.position - hitPoint)
            diffuse_scale = glm.max(glm.dot(self.obj.getNormal(hitPoint), light_dir), 0.0)
            diffuse = diffuse_scale * direction_light.color

            reflect_dir = glm.reflect(-light_dir, self.obj.getNormal(hitPoint))
            view_dir = glm.normalize(np.array(camera.position - hitPoint))
            spec = glm.pow(glm.max(glm.dot(view_dir, reflect_dir), 0.0), self.specular_power)
            specular = self.specular_strength * spec * direction_light.color

            return (ambient + diffuse + specular) * self.color