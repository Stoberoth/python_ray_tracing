from pyglm import glm
from camera import Camera
import light
from materials.basic_material import BasicMaterial
from materials.blinn_phong_material import BlinnPhongMaterial
from materials.reflective_material import ReflectiveMaterial
from object.plane import Plane
from object.sphere import Sphere


global list_of_objects

list_of_objects = []

blinn_mat = BlinnPhongMaterial()

global max_depth
max_depth = 3

global direction_light
direction_light = light.Light(glm.vec3(0, 2, 3), glm.vec3(1.0,1.0,1.0))

global camera
camera = Camera(focal_length=1)
camera.setupmatrix(position=[0.0,0.0,-2.0], target=glm.vec3(0,0,1))


s = Sphere(glm.vec3(0,0,4), 1, ReflectiveMaterial())
s1 = Sphere(glm.vec3(2,0,2), 1, BlinnPhongMaterial(color=[1.0,1.0,1.0]))

p1 = Plane(glm.vec3(5,0,0), glm.vec3(-1,0,0),BasicMaterial([1.0,0.0,0.0]))
#p2 = Plane(glm.vec3(-505,0,0), glm.vec3(1,0,0),BasicMaterial([0.0,0.0,1.0]))
p2 = Plane(glm.vec3(-5,0,0), glm.vec3(1,0,0),BlinnPhongMaterial(color=[0.0,0.0,1.0]))
p3 = Plane(glm.vec3(0,3,0), glm.vec3(0,-1,0),BasicMaterial([1.0,0.0,1.0]))
#p3 = Plane(glm.vec3(0,5,0), glm.vec3(0,-1,0),BasicMaterial([1.0,0.0,1.0]))
p4 = Plane(glm.vec3(0,-3,0), glm.vec3(0,1,0),ReflectiveMaterial())
#p4 = Plane(glm.vec3(0,-3,0), glm.vec3(0,1,0),BasicMaterial([1.0,1.0,.0]))
p5 = Plane(glm.vec3(0,0,-5), glm.vec3(0,0,1),BasicMaterial([0.0,1.0,1.0]))
p6 = Plane(glm.vec3(0,0,5), glm.vec3(0,0,-1),BasicMaterial([0.0,1.0,0.0]))
#p6 = Plane(glm.vec3(0,0,5), glm.vec3(0,0,-1),ReflectiveMaterial())

list_of_objects.append(s)
list_of_objects.append(s1)
#l.append(s1)
list_of_objects.append(p1)
list_of_objects.append(p2)
list_of_objects.append(p3)
list_of_objects.append(p4)
list_of_objects.append(p5)
list_of_objects.append(p6)