from pyglm import glm

class Ray:
    origin = glm.vec3()
    dir = glm.vec3()

    def __init__(self, origin, dir):
        self.origin = origin
        self.dir = dir


    def origin(self):
        return self.origin
    
    def dir(self):
        return self.dir
    
    # get a point on the ray
    def ray_cast(self, t):
        return self.origin + t * self.dir
    
