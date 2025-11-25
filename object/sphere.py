import sys

from numpy.core.defchararray import center
from camera import Camera
from object.object import Object
import ray
from pyglm import glm
import math
import numpy as np

# TODO : avoir une correction du hitPoint pour la refraction ici ou dans le materiel à voir

class Sphere(Object):
    center = glm.vec3(0.0,0.0,0.0)
    radius = 1.0
    color = [0,0,0]

    def __init__(self, center, radius, mat):
        super().__init__()
        self.center = center
        self.radius = radius
        self.mat = mat
        self.mat.obj = self
        
    
    def hit(self, ray: ray.Ray):
        super().hit(ray)
        oc = glm.vec3(ray.origin - self.center)
        a = glm.dot(ray.dir,ray.dir)
        b = 2.0 * glm.dot(ray.dir, oc)
        c = glm.dot(oc, oc) - self.radius * self.radius
        discriminant = b*b-4*a*c
        if(discriminant >=0):
            x1 = (-b+math.sqrt(discriminant))/(2*a)
            x2 = (-b-math.sqrt(discriminant))/(2*a)
            if x2 < 0 and x1 < 0:
                return None, None
            elif x2 <= 0:
                return x1, self
            else:
                return x2, self
        else:
            return None, None

    def getColor(self, hitPoint, r, depth):
        super().getColor(hitPoint, depth)
        #color = np.array(self.color) * glm.dot(glm.normalize(light.getPosition() - hitPoint), self.getNormal(hitPoint))
        #color = BlinnPhong(hitPoint, light, glm.normalize(glm.vec3(np.array(camera.position) - hitPoint)), self.getNormal(hitPoint), self.color)
        color = self.mat.computeColor(hitPoint, r, depth)
        return color

    def getNormal(self, point):
        super().getNormal(point)
        return glm.normalize(np.array(point) - np.array(self.center))
    
    