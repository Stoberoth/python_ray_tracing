from random import randrange
import random
import sys
from pyglm import glm

from object.object import Object
import ray
import numpy as np
from PIL import Image


class Camera:

    focal_length = 1

    aspect_ratio = 16.0/9.0
    screen_width = 800
    screen_height = int(screen_width / aspect_ratio)

    viewport_height = 0
    viewport_width = 0

    pixel_delta_u = 0
    pixel_delta_v = 0

    viewport_upper_left_center = [0.0,0.0,0.0]
    position = glm.vec3(0,0,0)

    def __init__(self, focal_length, position):
        self.focal_length = focal_length
        self.position = position
    
    def configure_viewport(self, viewport_height):
        self.viewport_height = viewport_height
        self.viewport_width = viewport_height * (self.screen_width / self.screen_height)
        viewport_u = glm.vec3(self.viewport_width, 0.0, 0.0)
        viewport_v = glm.vec3(0.0, -self.viewport_height, 0.0)
        self.pixel_delta_u = viewport_u / self.screen_width
        self.pixel_delta_v = viewport_v / self.screen_height

        viewport_upper_left = self.position - glm.vec3(0.0, 0.0, self.focal_length) - (viewport_u / 2.0) - (viewport_v / 2.0)
        self.viewport_upper_left_center = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v) 

    def save_image(self,image):
        rgb_image = (np.clip(image, 0.0,1.0) * 255.0).astype(np.uint8)
        new_image = Image.fromarray(rgb_image)
        new_image.save('image_with.png')

    def antialising(self,pixel_center, nb_samples, objects):
        color = np.array([0.0,0.0,0.0])
        for i in range(nb_samples):
            new_point = pixel_center + (random.random() - 0.5) * self.pixel_delta_u + (random.random() - 0.5) * self.pixel_delta_v
            ray_direction = glm.normalize(new_point - self.position)
            r = ray.Ray(self.position, ray_direction)
            min = sys.float_info.max
            minObj = None
            for o in objects:
                if o.hit(r) != None and min > o.hit(r):
                    min = o.hit(r)
                    minObj = o
            if(minObj != None):
                color += np.array(minObj.getColor())
        return np.array(color)/nb_samples

    def render_image(self, objects: list[Object]):
        print("Rendering ....")
        print(self.screen_height)
        print(self.screen_width)
        image = np.zeros((int(self.screen_height), int(self.screen_width), 3), dtype=np.int8)
        for j in range(self.screen_height):
            for i in range(self.screen_width):
                pixel_center = self.viewport_upper_left_center + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                color = [0.0,0.0,0.0]
                color = self.antialising(pixel_center, 20, objects)
                image[j,i] = color
                #image[j,i] = color
        
        self.save_image(image)
