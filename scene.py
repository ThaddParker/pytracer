import random

from cameras.camera import Camera
from ray import Ray
from utils.color import Colors, Color
from utils.image import Image


from utils.vector import Vector


class Scene:
    """Scene has all the information needed for the ray tracing engine"""

    def __init__(self, settings, camera: Camera, objects, lights):
        self.settings = settings
        self.camera = camera
        self.objects = objects
        self.lights = lights
        # self.width = settings.width
        # self.height = settings.height

    def render(self):
        image = Image(self.settings.width, self.settings.height)
        for j in range(self.settings.height):

            for i in range(self.settings.width):

                pixel_color = Colors.Black
                for s in range(self.settings.samples_per_pixel):
                    u = float(i) / self.settings.width
                    v = float(j) / self.settings.height
                    ray = self.camera.create_camera_ray(u, v)
                    pixel_color += self.ray_color(ray, self, self.settings.max_depth)
                image.set_pixel(i, j, pixel_color)
                print("{:3.0f}%".format(float(j) / float(self.settings.height) * 100), end="\r")

        print("Done...")
        with open("test.ppm", "w") as img_file:
            image.write_ppm(img_file)

    def ray_color(self, ray, scene, depth):
        if depth <= 0.:
            return Colors.Black

        if scene.objects:
            for obj in scene.objects:
                found, isect = obj.intersects(ray)
                if found:
                    target = isect.point + isect.normal + Vector.random_in_unit_sphere()
                    color = isect.object.material.color
                    n = isect.normal
                    return 0.5 * (self.ray_color(Ray(isect.point, target - isect.point), scene, depth-1))
                    # return sphere.material.color

        # background (could be a gradient map on the -Y axis
        norm = ray.direction.normalize()
        t = 0.5 * (norm.y + 1)
        return (1.-t)*Color(1.,1.,1.) + t*Color(0.5,0.7,1.)
