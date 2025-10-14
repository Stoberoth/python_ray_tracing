from pyglm import glm
from PIL import Image
import numpy as np

import ray

def hit_sphere(sphere_center, sphere_radius, r):
    oc = glm.vec3(sphere_center - r.origin)
    a = glm.dot(r.dir, r.dir)
    b = -2.0 * glm.dot(r.dir, oc)
    c = glm.dot(oc, oc) - sphere_radius * sphere_radius
    discriminant = b*b-4*a*c
    return discriminant >= 0

def ray_color(r) :
    if hit_sphere([0,0,-1], 0.5, r):
        return [1.0,0.0,0.0]

    unit_direction = r.dir
    a = 0.5*(unit_direction.y + 1.0)
    return (1.0-a)*np.array([1.0, 1.0, 1.0]) + a*np.array([0.0, 0.0, 0.0])

screen_width = 800

aspect_ratio = 16.0/9.0
screen_height = int(screen_width / aspect_ratio)
if screen_height < 1 :
    screen_height = 1

# camera 
# distance de l'écran rapport a la caméra
focal_length = 1
# hauteur de l'écran
viewport_height = 2.0
# largeur de l'écran
viewport_width = viewport_height * (screen_width / screen_height)
camera_center = glm.vec3(0.0,0.0,0.0)

# compute the vectors across the horizontal and down the vertical viewport edge
viewport_u = glm.vec3(viewport_width, 0.0, 0.0)
viewport_v = glm.vec3(0.0, -viewport_height, 0.0)

# calculate the horizontal delta from pixel to pixel (vecteur unitaire)
pixel_delta_u = viewport_u / screen_width
pixel_delta_v = viewport_v / screen_height

# compute the location of the upper left pixel 
viewport_upper_left = camera_center - glm.vec3(0.0, 0.0, focal_length) - viewport_u / 2.0 - viewport_v / 2.0
viewport_upper_left_center = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

image = np.empty((int(screen_height), int(screen_width), 3), dtype=np.float32)

# Render image
for j in range(int(screen_height)):
    for i in range(int(screen_width)):
        pixel_center = viewport_upper_left_center + (i * pixel_delta_u) + (j * pixel_delta_v)
        ray_direction = pixel_center - camera_center
        ray_direction = glm.normalize(ray_direction)
        r = ray.Ray(camera_center, ray_direction)
        color_pixel = ray_color(r)
        image[j, i] = color_pixel

rgb_image = (np.clip(image, 0.0, 1.0) * 255.0).astype(np.uint8)
new_image = Image.fromarray(rgb_image)
new_image.save('new.png')



