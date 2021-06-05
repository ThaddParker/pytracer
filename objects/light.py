from utils.color import Color


class Light:
    """Light represents a ipoint light source of a certain color"""

    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color


class PointLight(Light):
    pass


class AreaLight(Light):
    pass
