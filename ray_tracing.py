from pyglm import glm
from PIL import Image
import numpy as np

from camera import Camera
from object.plane import Plane
from object.sphere import Sphere
import ray


s = Sphere(glm.vec3(0,0,4), 1, [1.0,1.0,1.0])
s1 = Sphere(glm.vec3(505,0,0), 500, [1.0,0.0,0.0])
s2 = Sphere(glm.vec3(-505,0,0), 500, [0.0,0.0,1.0])
s3 = Sphere(glm.vec3(0,505,0), 500, [1.0,0.0,1.0])
s4 = Sphere(glm.vec3(0,-505,0), 500, [1.0,1.0,0.0])
s5 = Sphere(glm.vec3(0,0,-510), 500, [0.0,1.0,1.0])
s6 = Sphere(glm.vec3(0,0,510), 500, [0.0,1.0,0.0])

p1 = Plane(glm.vec3(505,0,0), glm.vec3(1,0,0),[1.0,0.0,0.0])
p2 = Plane(glm.vec3(-505,0,0), glm.vec3(-1,0,0),[0.0,0.0,1.0])
p3 = Plane(glm.vec3(0,505,0), glm.vec3(0,1,0),[1.0,0.0,1.0])
p4 = Plane(glm.vec3(0,-505,0), glm.vec3(0,-1,0),[1.0,1.0,0.0])
p5 = Plane(glm.vec3(0,0,-600), glm.vec3(0,0,-1),[0.0,1.0,1.0])
p6 = Plane(glm.vec3(0,0,600), glm.vec3(0,0,1),[0.0,1.0,0.0])

l = []

'''
l.append(s1)
l.append(s2)
l.append(s3)
l.append(s4)
l.append(s5)
l.append(s6)
'''

l.append(s)

l.append(p1)
l.append(p2)
l.append(p3)
l.append(p4)
l.append(p5)
l.append(p6)


camera = Camera(focal_length=1, position=[0.0,0.0,0.0])
camera.configure_viewport(viewport_height= 2.0)
camera.render_image(l)



