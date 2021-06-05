from material import Material
from ray import Ray
from utils.vector import Vector


class Plane:
    def __init__(self, normal_vector=Vector(0, 1.0, 0), distance=0.0, material=Material()):
        self.normal_vector = normal_vector
        self.distance = distance
        self.material = material

    def normal(self, surface_point):
        return self.normal_vector

    def intersects(self, ray: Ray):
        # d = ray.direction.dot(self.normal())
        return self.normal_vector.dot(ray.origin)
