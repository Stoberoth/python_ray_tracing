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

        viewport_upper_left = self.position - glm.vec3(0.0, 0.0, -self.focal_length) - (viewport_u / 2.0) - (viewport_v / 2.0)
        self.viewport_upper_left_center = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v) 

    def save_image(self,image):
        rgb_image = (np.clip(image, 0.0,1.0) * 255.0).astype(np.uint8)
        new_image = Image.fromarray(rgb_image)
        new_image.save('image.png')

    def render_image(self, objects: list[Object]):
        print("Rendering ....")
        print(self.screen_height)
        print(self.screen_width)
        image = np.empty((int(self.screen_height), int(self.screen_width), 3), dtype=np.float32)
        color = [0.0,0.0,0.0]
        for j in range(self.screen_height):
            for i in range(self.screen_width):
                pixel_center = self.viewport_upper_left_center + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                ray_direction = pixel_center - self.position
                r = ray.Ray(self.position, ray_direction)
                color = (ray_direction + glm.vec3(1.0, 1.0, 1.0)) * 0.5
                for o in objects:
                    if o.hit(r):
                        color = o.getColor()
                image[j,i] = color
        
        self.save_image(image)
