from pyglm import glm
from PIL import Image
import numpy as np

import obj_parser

import light
import ray
from scene import camera, direction_light, list_of_objects
from object.triangle import Triangle
from octree import Octree

#camera.render_image(list_of_objects, direction_light)


camera.render_image(list_of_objects, direction_light)
    
