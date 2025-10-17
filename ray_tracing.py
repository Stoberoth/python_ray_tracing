from pyglm import glm
from PIL import Image
import numpy as np

from camera import Camera
from object.object import Object
from object.sphere import Sphere
import ray

'''
def hit_sphere(sphere_center, sphere_radius, r):
    oc = glm.vec3(sphere_center - r.origin)
    a = glm.dot(r.dir, r.dir)
    b = -2.0 * glm.dot(r.dir, oc)
    c = glm.dot(oc, oc) - sphere_radius * sphere_radius
    discriminant = b*b-4*a*c
    return discriminant >= 0


def ray_color(r, color) :
    if hit_sphere([0,0,-1], 0.5, r):
        return [1.0,0.0,0.0]
    return np.array(color)
'''
s = Sphere(glm.vec3(0,0,-1), 0.5)

l = list[Object]()
l.append(s)

camera = Camera(focal_length=1, position=[0.0,0.0,0.0])
camera.configure_viewport(viewport_height= 2.0)
camera.render_image(l)



