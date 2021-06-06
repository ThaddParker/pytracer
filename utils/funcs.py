"""
Global functions
"""
import math
import random
import numpy as np



def random_double():
    r = np.random.MT19937(555)
    g = np.random.Generator(r)
    return g.uniform()

def random_doubleminmax(_min_, _max_):
    return _min_ + (_max_ - _min_) *random_double()


def clamp(x, _min_, _max_):
    if x < _min_:
        return _min_
    if x > _max_:
        return _max_
    return x



def degrees_to_radians(degrees):
    return degrees * math.pi / 180.


def fresnel_r(cos_ti, n):
    """
    // NB: This is a special case of the Fresnel formula, presuming that incident light is unpolarized.
    //
    // The implemented formula is as follows:
    //
    //      1     / g - cos Ti \ 2    /     / cos Ti (g + cos Ti) - 1 \ 2 \
    // R = --- * ( ------------ )  * ( 1 + ( ------------------------- )   )
    //      2     \ g + cos Ti /      \     \ cos Ti (g - cos Ti) + 1 /   /
    //
    // where
    //
    //        /---------------------------
    // g = -\/ (n1/n2)^2 + (cos Ti)^2 - 1
    """
    sqr_g = n ** 2 + cos_ti ** 2 - 1.
    if sqr_g <= 0.0:
        # total reflection
        return 1.0

    g = math.sqrt(sqr_g)
    quotient1 = (g - cos_ti) / (g + cos_ti)
    quotient2 = (cos_ti * (g + cos_ti) - 1.) / (cos_ti * (g - cos_ti) + 1.)
    f = 0.5 * quotient1 ** 2 * (1. + quotient2 ** 2)
    return np.clip(f, 0., 1.)


def compute_metallic(color, metallic_value, metallic_color, cos_angle):
    """
    // Calculate the reflected color by interpolating between
    // the light source color and the surface color according
    // to the (empirical) Fresnel reflectivity function.
    """
    if metallic_value != 0.:
        x = math.fabs(math.acos(cos_angle)) / (math.pi / 2.)
        f = 0.014567225 / ((x - 1.12) ** 2) - 0.011612903
        f = np.fmin(1., np.fmax(0., f))
        color *= (1. + (metallic_value * (1. - f)) * (metallic_color - 1.))

    return color


def compute_fresnel(reflective_color, reflection_max, reflection_min, cos_angle, ior):
    f = fresnel_r(cos_angle, ior)
    reflective_color = f * reflection_max + (1. - f) * reflection_min
    return reflective_color
