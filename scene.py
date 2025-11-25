from pyglm import glm
from camera import Camera
import light
from materials.basic_material import BasicMaterial
from materials.blinn_phong_material import BlinnPhongMaterial
from materials.fresnel_material import FresnelMaterial
from materials.reflective_material import ReflectiveMaterial
from object.plane import Plane
from object.sphere import Sphere

import obj_parser
from octree import Octree


global list_of_objects

list_of_objects = []

blinn_mat = BlinnPhongMaterial()

global max_depth
max_depth = 5

global direction_light
direction_light = light.Light(glm.vec3(0, 2, 2), glm.vec3(1.0,1.0,1.0))

global camera
camera = Camera(focal_length=1)
camera.setupmatrix(position=[0.0,0.0,0.0], target=glm.vec3(0,0,1))


s = Sphere(glm.vec3(0,0,4), 1,  BasicMaterial(color=[1.0,1.0,1.0]))
s1 = Sphere(glm.vec3(0,0,2), 1, FresnelMaterial(refract_index=1.0, color=[1.0,1.0,1.0]))
s2 = Sphere(glm.vec3(-2,0,2), 0.5, FresnelMaterial(refract_index=1.33, color=[0.5,0.5,0.5]))
s3 = Sphere(glm.vec3(2,0,2), 0.5, FresnelMaterial(refract_index=0, color=[1.0,1.0,1.0]))

p1 = Plane(glm.vec3(5,0,0), glm.vec3(-1,0,0),BasicMaterial([1.0,0.0,0.0]))
#p2 = Plane(glm.vec3(-505,0,0), glm.vec3(1,0,0),BasicMaterial([0.0,0.0,1.0]))
p2 = Plane(glm.vec3(-5,0,0), glm.vec3(1,0,0),BlinnPhongMaterial(color=[0.0,0.0,1.0]))
p3 = Plane(glm.vec3(0,3,0), glm.vec3(0,-1,0),BasicMaterial([1.0,0.0,1.0]))
#p3 = Plane(glm.vec3(0,5,0), glm.vec3(0,-1,0),BasicMaterial([1.0,0.0,1.0]))
#p4 = Plane(glm.vec3(0,-3,0), glm.vec3(0,1,0),ReflectiveMaterial())
p4 = Plane(glm.vec3(0,-3,0), glm.vec3(0,1,0),BasicMaterial([1.0,1.0,.0]))
p5 = Plane(glm.vec3(0,0,-5), glm.vec3(0,0,1),BasicMaterial([0.0,1.0,1.0]))
#p5 = Plane(glm.vec3(0,0,-5), glm.vec3(0,0,1),FresnelMaterial(refract_index=1.0,color=[1.0,1.0,1.0]))
p6 = Plane(glm.vec3(0,0,5), glm.vec3(0,0,-1),BasicMaterial([0.0,1.0,0.0]))
#p6 = Plane(glm.vec3(0,0,5), glm.vec3(0,0,-1),ReflectiveMaterial())
bunny = obj_parser.parse_obj("./resources/bunny.obj")

bunny.translate(glm.vec3( 0.0, -1.0, 4.0))
bunny.scale_uniform(10.0)
bunny.rotate_y(180)
bunny.generate_triangles()
octree = Octree(bunny)
octree.generate_octree()

list_of_objects.append(octree)


# list_of_objects.append(s)
# list_of_objects.append(s1)
# list_of_objects.append(s2)
# list_of_objects.append(s3)
list_of_objects.append(p1)
list_of_objects.append(p2)
list_of_objects.append(p3)
list_of_objects.append(p4)
list_of_objects.append(p5)
list_of_objects.append(p6)




