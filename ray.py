from utils.vector import Vector


class Ray:
    """Ray is a half-line with an origin and a normalized direction"""

    def __init__(self, origin: Vector, direction: Vector):
        self.origin = origin
        self.direction = direction
