from pyglm import glm
import sys

from materials.basic_material import BasicMaterial
from object.object import Object
from object.plane import Plane

class Cell:

    def generate_planes(self):
        mid = (self.min + self.max) / 2.0
        self.planes.append(Plane( glm.vec3(self.min.x, mid.y, mid.z), glm.vec3(1.0,0.0,0.0),BasicMaterial(color=[1.0,1.0,1.0])))
        self.planes.append(Plane(glm.vec3(self.max.x, mid.y, mid.z),glm.vec3(-1.0,0.0,0.0),  BasicMaterial(color=[1.0,1.0,1.0])))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.min.z),glm.vec3(0.0,1.0,0.0),  BasicMaterial(color=[1.0,1.0,1.0])))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, mid.z),glm.vec3(0.0,-1.0,0.0),  BasicMaterial(color=[1.0,1.0,1.0])))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.min.z),glm.vec3(0.0,0.0,1.0),  BasicMaterial(color=[1.0,1.0,1.0])))
        self.planes.append(Plane(glm.vec3(mid.x, mid.y, self.max.z),glm.vec3(0.0,0.0,-1.0),  BasicMaterial(color=[1.0,1.0,1.0])))
        
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.triangles = []
        self.planes = []
        self.children = []
        self.generate_planes()
    
    def hit(self, ray):
        triangles_in_cell = []
        if len(self.triangles) > 0:
            return self.triangles
        touch_cell = False
        for plane in self.planes:
            # on test si on touche un cellules ou pas 
            t, o = plane.hit(ray)
            eps = sys.float_info.epsilon
            if t == None:
                continue
            if t < -eps:
                continue
            p = ray.ray_cast(t)
            if (p.x >= self.min.x - eps and p.x <= self.max.x + eps and
                p.y >= self.min.y - eps and p.y <= self.max.y + eps and
                p.z >= self.min.z - eps and p.z <= self.max.z + eps):
                touch_cell = True
                break
        if touch_cell:
            for c in self.children:
                list_t = c.hit(ray)
                for tri in list_t:
                    triangles_in_cell.append(tri)
        return triangles_in_cell

class Octree(Object):
    model = None
    min = glm.vec3(0.0,0.0,0.0)
    max = glm.vec3(0.0,0.0,0.0)
    num_cells = 0
    max_depth = 10
    root = None

    planes = []
    
    def compute_boundingBox(self):
        min = glm.vec3(sys.float_info.max, sys.float_info.max, sys.float_info.max)
        max = glm.vec3(-sys.float_info.max, -sys.float_info.max, -sys.float_info.max)
        for v in self.model.vertices:
            if v.x < min.x:
                min.x = v.x
            if v.y < min.y:
                min.y = v.y
            if v.z < min.z:
                min.z = v.z
            if v.x > max.x:
                max.x = v.x
            if v.y > max.y:
                max.y = v.y
            if v.z > max.z:
                max.z = v.z
        self.min = min
        self.max = max

    def __init__(self, model, mat=None):
        self.model = model
        # generate the bounding box
        self.compute_boundingBox()
        self.root = Cell(self.min, self.max)
        self.num_cells = 1
        self.root.triangles = self.model.triangles
    
    def isInCell(self, triangle, cell):
        barycentre = glm.vec3(0.0)
        # for v in triangle.vertices:
        #     barycentre += v
        # barycentre /= 3.0
        # if barycentre.x >= cell.min.x and barycentre.x <= cell.max.x and barycentre.y >= cell.min.y and barycentre.y <= cell.max.y and barycentre.z >= cell.min.z and barycentre.z <= cell.max.z:
        #     return True
        eps = 1e-12
        for v in triangle.vertices:
            if (v.x >= cell.min.x - eps and v.x <= cell.max.x + eps and
                v.y >= cell.min.y - eps and v.y <= cell.max.y + eps and
                v.z >= cell.min.z - eps and v.z <= cell.max.z + eps):
                return True
        return False

    def subdivide_cell(self, cell, depth):
       # print("dividing cell at depth ", depth, " with ", len(cell.triangles), " triangles")
        if depth >= self.max_depth or len(cell.triangles) <= 100:
            return
        mid = (cell.min + cell.max) / 2
        # eps = 1e-12
        # if (abs(mid.x - cell.min.x) < eps or abs(mid.y - cell.min.y) < eps or abs(mid.z - cell.min.z) < eps or
        #     abs(cell.max.x - mid.x) < eps or abs(cell.max.y - mid.y) < eps or abs(cell.max.z - mid.z) < eps):
        #     return
        # create 8 children cells
        cell.children = []
        cell.children.append(Cell(cell.min, mid)) # en bas à gauche premier plan
        cell.children.append(Cell(glm.vec3(mid.x, cell.min.y, cell.min.z), glm.vec3(cell.max.x, mid.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, cell.min.y, mid.z), glm.vec3(cell.max.x, mid.y, cell.max.z)))
        cell.children.append(Cell(glm.vec3(cell.min.x, cell.min.y, mid.z), glm.vec3(mid.x, mid.y, cell.max.z)))
        
        cell.children.append(Cell(glm.vec3(cell.min.x, mid.y, cell.min.z), glm.vec3(mid.x, cell.max.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, mid.y, cell.min.z), glm.vec3(cell.max.x, cell.max.y, mid.z)))
        cell.children.append(Cell(glm.vec3(mid.x, mid.y, mid.z), glm.vec3(cell.max.x, cell.max.y, cell.max.z)))
        cell.children.append(Cell(glm.vec3(cell.min.x, mid.y, mid.z), glm.vec3(mid.x, cell.max.y, cell.max.z)))
        
        for triangle in list(cell.triangles):
            for c in cell.children:
                if self.isInCell(triangle, c):
                    c.triangles.append(triangle)
        cell.triangles = []
        for c in cell.children:
            self.subdivide_cell(c, depth +1)
    
    

    def generate_octree(self):
        self.subdivide_cell(self.root, 0)

    def hit(self, r):
        super().hit(r)
        list_of_triangle = self.root.hit(r)
        min_t = sys.float_info.max
        min_triangle = None
        for tri in list_of_triangle:
            t = tri.hit(r)
            eps = 1e-12
            if t is not None and t > eps and t < min_t:
                min_t = t
                min_triangle = tri
        return min_t, min_triangle

    
    def getNormal(self, point):
        return super().getNormal(point)
    def getColor(self, hitPoint,r, depth):
        return super().getColor(hitPoint, r, depth)
        
