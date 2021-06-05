from utils.color import Color, Colors
from objects.sphere import Sphere
from objects.light import Light
from material import Material, Finish
from cameras.camera import PerspectiveCamera
from utils.vector import Vector

WIDTH = 300
HEIGHT = 300
RENDERED_IMG = "2balls.ppm"
CAMERA = PerspectiveCamera(location=Vector(0, -1.5, -5))
OBJECTS = [
    # Ground Plane
    Sphere(
        Vector(0, 10000.5, 1),
        10000.0,
        Material(modifiers={"checkered": True, "color2": Color.from_hex("#e6b87d")},
                 color=Color.from_hex("#420500"),
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
    Sphere(Vector(0.75, -0.1, 1), 0.6, Material(Colors.Blue)),
    # Pink ball
    Sphere(Vector(-0.75, -0.1, 2.25), 0.6, Material(Color.from_hex("#803980"))),
]
LIGHTS = [
    Light(Vector(1.5, -0.5, -10), Colors.White),
    Light(Vector(-0.5, -10.5, 0), Color.from_hex("#E6E6E6"))
]
