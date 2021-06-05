#!/usr/bin/env python
"""Puray - a Pure Python Raytracer by Arun Ravindran, 2019"""
import argparse
import importlib
import os
import random
from multiprocessing import cpu_count

from cameras.camera import Camera
from engine import RenderEngine
from includes.settings import Settings
from material import Material
from objects.sphere import Sphere
from ray import Ray
from scene import Scene
from utils.color import Color, Colors
from utils.vector import Vector
from utils.image import Image


def main1():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Path to scene file (without .py extension)")

    args = parser.parse_args()
    if args.processes == 0:
        process_count = cpu_count()
    else:
        process_count = args.processes

    mod = importlib.import_module(args.scene)
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()

    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, "w") as img_fileobj:
        engine.render_multiprocess(scene, process_count, img_fileobj)

def main():
    settings = Settings()
    camera = Camera()
    objs = [Sphere(Vector(0, 0, -1), 0.5, Material(Colors.Red))]
    scene = Scene(None,camera,objs,None)

    def ray_color(ray, obj):

        found, isect = obj.intersects(ray)
        if found:
            target = isect.point + isect.normal + Vector.random_in_unit_sphere()
            color = isect.object.material.color
            n = isect.normal
            return 0.5 * (ray_color(Ray(isect.point, target - isect.point), obj))
            # return sphere.material.color

        # background (could be a gradient map on the -Y axis
        norm = ray.direction.normalize()
        t = 0.5 * (norm.y - 1)
        return (1.-t)*Color(1.,1.,1.) + t*Color(0.5,0.7,1.)

    aspect_ratio = 16. / 9.
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 10

    #render
    image = Image(image_width, image_height)
    for j in range(image_height):
        print("Scan lines left: " + str(j),end="\r")
        for i in range(image_width):

            pixel_color = Color(0,0,0)
            for s in range(samples_per_pixel):
                u = float(i + random.random()) / (image_width)
                v = float(j+ random.random()) / (image_height)
                ray = camera.create_camera_ray(u, v)
                pixel_color += ray_color(ray, sphere)
            image.set_pixel(i, j, pixel_color)
            print("{:3.0f}%".format(float(j) / float(image_height) * 100), end="\r")

    print("Done...")
    with open("test.ppm", "w") as img_file:
        image.write_ppm(img_file)


if __name__ == "__main__":
    main()
