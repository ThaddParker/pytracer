from utils.vector import Vector


class Ray:
    """Ray is a half-line with an origin and a normalized direction"""

    def __init__(self, origin: Vector = Vector(), direction: Vector = Vector(z=1.)):
        self.origin = origin
        self.direction = direction

    def __str__(self):
        return f"origin: {self.origin!s}\ndirection: {self.direction!s}"

    def __repr__(self):
        return f"Ray [origin: {self.origin!r}, direction: {self.direction!r}]"

    def evaluate(self, point):
        return self.origin + point * self.direction
