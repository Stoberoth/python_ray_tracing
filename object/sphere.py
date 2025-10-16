from object.object import Object
import ray
from pyglm import glm

class Sphere(Object):
    center = glm.vec3(0.0,0.0,0.0)
    radius = 1.0
    
    def hit(self, ray: ray.Ray):
        oc = glm.vec3(self.center - ray.origin)
        a = glm.dot(ray.dir, ray.dir)
        b = -2.0 * glm.dot(ray.dir, oc)
        c = glm.dot(oc, oc) - self.radius * self.radius
        discriminant = b*b-4*a*c
        return discriminant >= 0