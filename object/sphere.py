import sys

from numpy.core.defchararray import center
from camera import Camera
from lighting import BlinnPhong
from object.object import Object
import ray
from pyglm import glm
import math
import numpy as np

class Sphere(Object):
    center = glm.vec3(0.0,0.0,0.0)
    radius = 1.0
    color = [0,0,0]

    def __init__(self, center, radius, color):
        super().__init__()
        self.center = center
        self.radius = radius
        self.color = color
        
    
    def hit(self, ray: ray.Ray):
        super().hit(ray)
        oc = glm.vec3(ray.origin - self.center)
        a = glm.dot(ray.dir, ray.dir)
        b = 2.0 * glm.dot(ray.dir, oc)
        c = glm.dot(oc, oc) - self.radius * self.radius
        discriminant = b*b-4*a*c
        if(discriminant >=0):
            x1 = (-b+math.sqrt(discriminant))/(2*a)
            x2 = (-b-math.sqrt(discriminant))/(2*a)
            if x2 < 0 and x1 < 0:
                return None
            elif x2 < 0:
                return x1
            else:
                return x2
        else:
            return None

    def getColor(self, light, hitPoint, camera: Camera):
        super().getColor(light, hitPoint, camera)
        color = np.array(self.color) * glm.dot(glm.normalize(light.getPosition() - hitPoint), self.getNormal(hitPoint))
        color = BlinnPhong(hitPoint, light, glm.normalize(glm.vec3(np.array(camera.position) - hitPoint)), self.getNormal(hitPoint), self.color)
        return color

    def getNormal(self, point):
        super().getNormal(point)
        return glm.normalize(np.array(point) - np.array(self.center))
    
    