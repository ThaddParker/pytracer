from utils.color import Color


class Finish:
    """Finish is how the reaction to light coupled with Material"""

    def __init__(self, ambient=0.1, diffuse=0.6, diffuse_back=0.0, brilliance=1.0, specular=0.0,
                 reflection=0.5,
                 roughness=1.0/0.05, phong=0.0, phong_size=40, metallic=0.0, emission=0.0,
                 reflection_max=0.0,
                 reflection_min=0.0, reflection_falloff=1, reflection_metallic=0.0, fresnel=0.0):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.diffuse_back = diffuse_back
        self.brilliance = brilliance
        self.roughness = roughness
        self.phong = phong
        self.phong_size = phong_size
        self.metallic = metallic
        self.emission = emission
        self.reflection_max = reflection_max
        self.reflection_min = reflection_min
        self.reflection_falloff = reflection_falloff
        self.reflection_metallic = reflection_metallic
        self.fresnel = fresnel


class Material:
    """Material has color and properties which tells us how it reacts to light"""

    def __init__(
            self,
            color=Color.from_hex("#FFFFFF"),
            finish: Finish = Finish()
    ):
        self.color = color
        self.finish = finish

    def color_at(self, position):
        return self.color


class CheckeredMaterial(Material):
    """Material which has a chessboard pattern based on two colors"""

    def __init__(self, color=Color.from_hex("#FFFFFF"), color2=Color.from_hex("#000000"), finish=Finish()):
        super().__init__(color, finish)

        self.color2 = color2

    def color_at(self, position):
        if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
            return self.color
        else:
            return self.color2
