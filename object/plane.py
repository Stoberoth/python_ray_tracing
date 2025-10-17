import sys
from object.object import Object
from pyglm import glm
import ray

class Plane(Object):
    attach_point = glm.vec3(0.0,0.0,0.0)
    normal = glm.vec3(0.0,0.0,0.0)
    color = [0.0,1.0,0.0]

    def __init__(self, attach_point, normal, color) :
        super().__init__()
        self.attach_point = attach_point
        self.normal = normal
        self.color = color

    def hit(self, r: ray.Ray):
        super().hit(r)
        '''
        denom = glm.dot(self.normal, r.dir)
        if denom > sys.float_info.epsilon:
            p0l0 = self.attach_point - r.origin
            t = glm.dot(p0l0, self.normal)
            if t >= 0:
                return t
            else:
                return None
        '''
        t = glm.dot((self.attach_point - r.origin), self.normal) / glm.dot(r.dir, self.normal)
        if(t >=0 ): 
            return t
        return None

    def getColor(self):
        super().getColor()
        return self.color