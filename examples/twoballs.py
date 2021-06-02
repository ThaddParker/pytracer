from utils.color import Color
import includes.colors as color
from light import Light
from material import CheckeredMaterial, Material, Finish
# from point import Point
from objects.sphere import Sphere
from vectormath import Vector3
from cameras.camera import PerspectiveCamera

WIDTH = 300
HEIGHT = 300
RENDERED_IMG = "2balls.ppm"
CAMERA = PerspectiveCamera(location=Vector3(0, -1.5, -5))
OBJECTS = [
    # Ground Plane
    Sphere(
        Vector3(0, 10000.5, 1),
        10000.0,
        CheckeredMaterial(
            color=Color.from_hex("#420500"),
            color2=Color.from_hex("#e6b87d"),
            finish=Finish(ambient=0.2, reflection=0.2)
        ),
    ),
    # Plane(
    #    Vector3(0, 0.5, 0),
    #    0.0,
    #    CheckeredMaterial(
    #     color=Color.from_hex("#420500"),
    #     color2=Color.from_hex("#e6b87d"),
    #     finish=Finish(ambient=0.2, reflection=0.2)
    #    ),
    #  ),
    # Blue ball
    Sphere(Vector3(0.75, -0.1, 1), 0.6, Material(color.BLUE)),
    # Pink ball
    Sphere(Vector3(-0.75, -0.1, 2.25), 0.6, Material(Color.from_hex("#803980"))),
]
LIGHTS = [
    Light(Vector3(1.5, -0.5, -10), color.WHITE),
    Light(Vector3(-0.5, -10.5, 0), Color.from_hex("#E6E6E6"))
]
