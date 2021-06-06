import random

from cameras.camera import Camera
from utils.funcs import *
from ray import Ray
from utils.color import Colors, Color
from utils.image import Image


from utils.vector import Vector
from includes.consts import Constants as consts


class Scene:
    """Scene has all the information needed for the ray tracing engine"""

    def __init__(self, settings, camera: Camera, objects, lights):
        self.settings = settings
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.width = settings.width
        self.height = settings.height

    def render(self):
        image = Image(self.settings.width, self.settings.height, self.settings.samples_per_pixel)
        for j in reversed(range(self.settings.height)):

            for i in range(self.settings.width):

                pixel_color = Colors.Black
                for _ in range(self.settings.samples_per_pixel):
                    u = float(i + random_double()) / self.width
                    v = float(j + random_double()) / self.height
                    ray = self.camera.create_camera_ray(u, v)
                    pixel_color += self.ray_color(ray, self, self.settings.max_depth)

                image.set_pixel(i, j, pixel_color)
                print("{:3.0f}%".format(math.fabs(-float(j) / float(self.height) * 100)), end="\r")

        print("Done...")
        with open("test.ppm", "w") as img_file:
            image.write_ppm(img_file)

    def ray_color(self, ray, scene, depth):
        if depth <= 0:
            return Colors.Black

        found, isect = self.find_intersection(ray, scene.objects,0.001, consts.MAX_DISTANCE)
        if found:
            scattered_ray = None
            attenuation = Colors.Black
            color_found, attenuation, scattered_ray = isect.object.material.color_at(isect=isect)
            if color_found:
                return attenuation * self.ray_color(scattered_ray, scene, depth-1)
            return Colors.Black
            # return sphere.material.color

        # background (could be a gradient map on the -Y axis
        norm = ray.direction.normalize()
        t = 0.5 * (norm.y + 1)
        return (1.-t)*Color(1.,1.,1.) + t*Color(0.5,0.7,1.)

    def find_intersection(self, ray, objects, min_distance=0.0001, max_distance=consts.MAX_DISTANCE):
        closest_so_far = max_distance
        hit_anything = False
        isectout = None
        if objects:
            for obj in objects:
                found, isect = obj.intersects(ray, closest_so_far, max_distance)
                if found:
                    hit_anything = found
                    closest_so_far = isect.distance
                    isectout = isect
        
        return hit_anything, isectout

