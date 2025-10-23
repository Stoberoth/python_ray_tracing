import sys
from object.object import Object
from pyglm import glm
import ray
import numpy as np

class Plane(Object):
    attach_point = glm.vec3(0.0,0.0,0.0)
    normal = glm.vec3(0.0,0.0,0.0)

    def __init__(self, attach_point, normal, mat) :
        super().__init__()
        self.attach_point = attach_point
        self.normal = normal
        self.mat = mat
        self.mat.obj = self

    def hit(self, r: ray.Ray):
        super().hit(r)
        t = -1
        if glm.dot(r.dir, self.normal) != 0:
            t = glm.dot((self.attach_point - r.origin), self.normal) / glm.dot(r.dir, self.normal)
        if(t >= 0): 
            return t
        return None

    def getColor(self, hitPoint,r, depth):
        super().getColor(hitPoint, depth)
        return self.mat.computeColor(hitPoint, r, depth)

    def getNormal(self, point):
        super().getNormal(point)
        return self.normal