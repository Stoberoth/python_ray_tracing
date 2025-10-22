from pyglm import glm

class Ray:
    origin = glm.vec3()
    dir = glm.vec3()

    def __init__(self, origin, dir):
        self.origin = origin
        self.dir = glm.normalize(dir)

    def get_origin(self):
        return self.origin
    
    def get_dir(self):
        return self.dir
    
    # get a point on the ray
    def ray_cast(self, t):
        return self.origin + t * self.dir
    
