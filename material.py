from utils.color import Color, Colors
from utils.funcs import *


class Finish:
    """Finish is how the reaction to light coupled with a Material"""

    def __init__(self, **kwargs):
        self.ambient = kwargs.get('ambient', Color(0.1, 0.1, 0.1))
        self.diffuse = kwargs.get('diffuse', 0.6)
        self.specular = kwargs.get('specular', 0.0)
        self.reflection = kwargs.get('reflection', 0.5)
        self.diffuse_back = kwargs.get('diffuse_back', 0.0)
        self.brilliance = kwargs.get('brilliance',1.0)
        self.brilliance_adjust = kwargs.get('brilliance_adjust', 1.0)
        self.roughness = kwargs.get('roughness', 1. /0.05)
        self.phong = kwargs.get('phong', 0.0)
        self.phong_size = kwargs.get('phong_size', 40)
        self.metallic = kwargs.get('metallic', 0.0)
        self.emission = kwargs.get('emission', Colors.Black)
        self.reflection_max = kwargs.get('reflection_max', Colors.Black)
        self.reflection_min = kwargs.get('reflection_min', Colors.Black)
        self.reflection_falloff = kwargs.get('reflection_falloff',1.)
        self.reflection_metallic = kwargs.get('reflection_metallic', 0.)
        self.fresnel = kwargs.get('fresnel',0.)
        self.iridescence = kwargs.get('irid', 0.0)
        self.iridescence_turbulence = kwargs.get('irid_turb', 0.)
        self.irid_film_thickness = kwargs.get('irid_film_thickness', 0.)



class Material:
    """Material has color and properties which tells us how it reacts to light"""

    def __init__(
            self,
            color=Color.from_hex("#FFFFFF"),
            finish: Finish = Finish(), modifiers=None
    ):
        if modifiers is None:
            modifiers = dict()
        self.color = color
        self.finish = finish
        self.modifiers = modifiers

    def color_at(self, ray, position):
        if self.modifiers is None:
            return self.color

    def compute_specular(self, light, ray, normal, relative_ior):
        light_color = light.color
        light_direction = light.direction
        reverse_eye_ray = -ray.direction
        intensity = 1.
        half_way = (reverse_eye_ray + light_direction) * 0.5
        half_way_length = half_way.length()
        if half_way_length > 0.:
            cos_angle_of_incidence = np.dot(half_way.to_array(), normal.to_array()) / half_way_length
            if cos_angle_of_incidence > 0.:
                intensity = self.finish.specular * math.pow(cos_angle_of_incidence, self.finish.roughness)
                if self.finish.fresnel != 0. or self.finish.metallic != 0.:
                    cs = Colors.White
                    ndotl = np.dot(half_way.to_array(), light_direction.to_array()) / half_way_length
                    if self.finish.fresnel != 0.:
                        cs *= self.finish.fresnel * fresnel_r(ndotl, relative_ior)
                    cs = compute_metallic(cs, self.finish.specular, self.color, ndotl)
                    return self.color + intensity * light_color * cs
            else:

                return self.color + intensity * light_color
        return self.color * light_color

    def compute_diffuse(self, light, ray, normal, relative_ior, attenuation, backside):
        diffuse = (self.finish.diffuse_back if backside else self.finish.diffuse) * self.finish.brilliance_adjust
        if diffuse <= 0.:
            return self.color
        cos_angle_of_incidence = np.dot(normal.to_array(), light.direction)
        # brilliance is likely to be 1.0 (default value)
        if self.finish.brilliance != 1.0:
            intensity = math.pow(math.fabs(cos_angle_of_incidence), self.finish.brilliance)
        else:
            intensity = math.fabs(cos_angle_of_incidence)
        intensity *= diffuse * attenuation

        if self.finish.fresnel != 0.:
            f1 = self.finish.fresnel * fresnel_r(cos_angle_of_incidence, relative_ior)
            cos_angle_of_incidence = -np.dot(normal.to_array(), -ray.direction.to_array())
            f2 = self.finish.fresnel * fresnel_r(cos_angle_of_incidence, relative_ior)
            return self.color + intensity * self.color * light.color * (1. - f1) * (1. - f2)
        else:
            return self.color + intensity * self.color * light.color

    def compute_phong(self, light, ray, normal, relative_ior):
        light_color = light.color
        light_direction = light.direction
        eye_direction = - ray.direction
        intensity = 1.0
        cos_angle_of_incidence = -2. * np.dot(eye_direction.to_array(), normal)
        if cos_angle_of_incidence > 0.:
            if self.finish.phong_size < 60 or cos_angle_of_incidence > 0.0008:
                intensity = self.finish.phong * math.pow(cos_angle_of_incidence, self.finish.phong_size)
                cs = Colors.White
                if self.finish.fresnel != 0. or self.finish.metallic != 0.:

                    ndotl = np.dot(normal, light_direction)

                    if self.finish.fresnel != 0.:
                        cs *= self.finish.fresnel * fresnel_r(ndotl, relative_ior)
                    cs = compute_metallic(cs, self.finish.metallic, self.color, ndotl)
                return self.color + intensity * light_color * cs
        else:
            return self.color + intensity * light_color
        return self.color * light_color

    def compute_iridescence(self, normal, ipoint):

        film_thickness = self.finish.irid_film_thickness
        if self.finish.iridescence_turbulence != 0:
            pass

        pass
