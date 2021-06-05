import numpy as np
import numbers


class Color:

    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def __str__(self):
        # Used for debugging. This method is called when you print an instance  
        return "(" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"

    def __repr__(self):
        return f"Color ({self.red!r},{self.green!r},{self.blue!r})"

    def __setitem__(self, key, value):
        if isinstance(key, int) and (isinstance(value, int) or isinstance(value, numbers.Number)):
            if key == 0:
                self.red = value
            elif key == 1:
                self.green = value
            elif key == 2:
                self.blue = value

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.red
            elif item == 1:
                return self.green
            elif item == 2:
                return self.blue
            else:
                return None
        return None

    def __add__(self, v):
        if isinstance(v, Color):
            return Color(self.red + v.red, self.green + v.green, self.blue + v.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red + v, self.green + v, self.blue + v)

    def __radd__(self, v):
        if isinstance(v, Color):
            return Color(self.red + v.red, self.green + v.green, self.blue + v.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red + v, self.green + v, self.blue + v)

    def __sub__(self, v):
        if isinstance(v, Color):
            return Color(self.red - v.red, self.green - v.green, self.blue - v.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red - v, self.green - v, self.blue - v)

    def __rsub__(self, v):
        if isinstance(v, Color):
            return Color(v.red - self.red, v.green - self.green, v.blue - self.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v - self.red, v - self.green, v - self.blue)

    def __mul__(self, v):
        if isinstance(v, Color):
            return Color(self.red * v.red, self.green * v.green, self.blue * v.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red * v, self.green * v, self.blue * v)

    def __rmul__(self, v):
        if isinstance(v, Color):
            return Color(v.red * self.red, v.green * self.green, v.blue * self.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v * self.red, v * self.green, v * self.blue)

    def __truediv__(self, v):
        if isinstance(v, Color):
            return Color(self.red / v.red, self.green / v.green, self.blue / v.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red / v, self.green / v, self.blue / v)

    def __rtruediv__(self, v):
        if isinstance(v, Color):
            return Color(v.red / self.red, v.green / self.green, v.blue / self.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v / self.red, v / self.green, v / self.blue)

    def __abs__(self):
        return Color(np.abs(self.red), np.abs(self.green), np.abs(self.blue))

    def __pow__(self, a):
        return Color(self.red ** a, self.green ** a, self.blue ** a)

    def to_array(self):
        return np.array([self.red, self.green, self.blue])

    def components(self):
        return self.red, self.green, self.blue

    def extract(self, cond):
        return Color(extract(cond, self.red),
                     extract(cond, self.green),
                     extract(cond, self.blue))

    @staticmethod
    def where(cond, out_true, out_false):
        return Color(np.where(cond, out_true.red, out_false.red),
                     np.where(cond, out_true.green, out_false.green),
                     np.where(cond, out_true.blue, out_false.blue))

    @staticmethod
    def select(mask_list, out_list):
        out_list_x = [i.x for i in out_list]
        out_list_y = [i.y for i in out_list]
        out_list_z = [i.z for i in out_list]

        return Color(np.select(mask_list, out_list_x),
                     np.select(mask_list, out_list_y),
                     np.select(mask_list, out_list_z))

    def clip(self, _min_, _max_):
        return Color(np.clip(self.red, _min_, _max_),
                     np.clip(self.green, _min_, _max_),
                     np.clip(self.blue, _min_, _max_))

    def place(self, cond):
        r = Color(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.red, cond, self.red)
        np.place(r.green, cond, self.green)
        np.place(r.blue, cond, self.blue)
        return r

    def mean(self, axis):
        return Color(np.mean(self.red, axis=axis), np.mean(self.green, axis=axis), np.mean(self.blue, axis=axis))

    def __eq__(self, other):
        return (self.red == other.x) & (self.green == other.y) & (self.blue == other.z)

    @staticmethod
    def array_to_color(array):
        return Color(array[0], array[1], array[2])

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)


class Colors:
    Black = Color(0., 0., 0.)
    White = Color(1., 1., 1.)
    Red = Color(1., 0., 0.)
    Green = Color(0., 1., 0.)
    Blue = Color(0., 0., 1.)
