from pyglm import glm
from PIL import Image
import numpy as np

import light
import ray
from scene import camera, direction_light, list_of_objects

camera.render_image(list_of_objects, direction_light)



