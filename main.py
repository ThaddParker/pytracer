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
from utils.color import Colors
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
    settings = Settings(samples=1)
    camera = Camera()
    objs = [Sphere(Vector(0, 0, -1), 0.5, Material(Colors.Red)),
            Sphere(Vector(0,-100.5,-1),100, Material(Colors.Green))
            ]
    scene = Scene(settings,camera,objs,None)



    #render
    scene.render()


if __name__ == "__main__":
    main()
