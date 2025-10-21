from random import randrange
import random
import sys
from turtle import position
from types import NoneType
from pyglm import glm

from lighting import BlinnPhong
from materials.reflective_material import ReflectiveMaterial
from object.object import Object
import light
import ray
import numpy as np
from PIL import Image


class Camera:

    focal_length = 1

    aspect_ratio = 16.0/9.0
    screen_width = 800
    screen_height = int(screen_width / aspect_ratio)
    position = [0,0,0]
    projection_matrix = glm.perspective(glm.radians(60), 16/9, 0.1, 100.0)

    eye_to_world_matrix = glm.mat4x4()

    def __init__(self, focal_length):
        self.focal_length = focal_length
    
    def setupmatrix(self,position, target):
        self.position = position
        view_matrix = glm.lookAt(position, target, [0,1,0])
        self.eye_to_world_matrix = glm.inverse(view_matrix)

    def save_image(self,image):
        rgb_image = (np.clip(image, 0.0,1.0) * 255.0).astype(np.uint8)
        new_image = Image.fromarray(rgb_image)
        new_image.save('image_shadow_on_miror.png')

  

    def antialising(self,pixel_center, nb_samples, objects, light):
        color = np.array([0.0,0.0,0.0])
        for i in range(nb_samples):
            #new_point = pixel_center + (random.random() - 0.5) * self.pixel_delta_u + (random.random() - 0.5) * self.pixel_delta_v
            '''
            ray_direction = glm.normalize(new_point - self.position)
            r = ray.Ray(self.position, ray_direction)
            '''
            x = glm.clamp(pixel_center[0] + (random.random() - 0.5), 0, self.screen_width)
            y = glm.clamp(pixel_center[1] + (random.random() - 0.5), 0, self.screen_height)
            r = self.generate_ray_with_matrix(x, y)
            min = sys.float_info.max
            minObj = None
            for o in objects:
                if o.hit(r) != None and min > o.hit(r):
                    min = o.hit(r)
                    minObj = o
            if(minObj != None):
                p = r.ray_cast(min)
                #normal = glm.normalize(minObj.getNormal(p))
                if(type(minObj.getColor(light, p, self, r, 0)) != NoneType):
                    color += np.array(minObj.getColor(light, p, self, r, 0))
                #color += BlinnPhong(p, lightPos, p, normal, minObj.getColor())
        return np.array(color) / nb_samples

    def generate_ray_with_matrix(self, i, j):
        pixel_normalize_x = (2.0 * i / self.screen_width) - 1.0
        pixel_normalize_y = 1.0 - (2.0 * j / self.screen_height)

        # point dans l'espace camera
        ray_eye = glm.vec4(pixel_normalize_x * self.aspect_ratio, pixel_normalize_y, -self.focal_length, 1.0)

        # camera to world
        ray_world_space = self.eye_to_world_matrix * ray_eye
        ray_dir = glm.normalize(ray_world_space.xyz - self.position)

        return ray.Ray(self.position, ray_dir)

    def render_image(self, objects: Object, light: light.Light):
        print("Rendering ....")
        print(self.screen_height)
        print(self.screen_width)
        image = np.zeros((int(self.screen_height), int(self.screen_width), 3), dtype=np.float32)
        for j in range(self.screen_height):
            for i in range(self.screen_width):
                color = self.antialising([i,j], 10, objects, light)
                image[j,i] = color
        
        self.save_image(image)
