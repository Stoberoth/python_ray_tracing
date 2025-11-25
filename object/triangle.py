from pyglm import glm
import sys

from object.object import Object

class Triangle(Object):

    def __init__(self, v0, v1, v2, mat=None, parent=None):
        super().__init__()
        self.vertices = [v0,v1,v2]
        self.mat = mat
        self.mat.obj = self
        self.parent = parent

    
    def hit(self, ray):
        super().hit(ray)
        edge1 = self.vertices[1] - self.vertices[0]
        edge2 = self.vertices[2] - self.vertices[0]

        pVec = glm.cross(glm.normalize(ray.dir), edge2)
        det = glm.dot(edge1, pVec)

        if abs(det) < sys.float_info.epsilon:
            return None
        
        invDet = 1.0 / det

        tVec = ray.origin - self.vertices[0]

        u = glm.dot(tVec, pVec) * invDet

        if u < 0.0 or u > 1.0:
            return None
        
        qVec = glm.cross(tVec, edge1)
        v = glm.dot(glm.normalize(ray.dir), qVec) * invDet
        if v < 0.0 or u+v > 1.0:
            return None
        
        p_t = glm.dot(edge2, qVec) * invDet
        p_uv = glm.vec2(u,v)
        if p_t > sys.float_info.epsilon:
            return p_t
    
    def getColor(self, hitPoint,r, depth):
        return self.mat.computeColor(hitPoint, r, depth)
    
    def getNormal(self, point):
        return glm.normalize(glm.cross(self.vertices[1]-self.vertices[0], self.vertices[2]-self.vertices[0]))