from random import  uniform

import numpy as np
import numbers


def extract(cond, x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return np.extract(cond, x)


class Vector:

    def __init__(self, x=0., y=0., z=0.):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        # Used for debugging. This method is called when you print an instance  
        return "<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">"

    def __repr__(self):
        return f"Vector <{self.x!r},{self.y!r},{self.z!r}>"

    def __setitem__(self, key, value):
        if isinstance(key, int) and (isinstance(value, int) or isinstance(value, numbers.Number)):
            if key == 0:
                self.x = value
            elif key == 1:
                self.y = value
            elif key == 2:
                self.z = value

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            elif item == 2:
                return self.z
            else:
                return None
        return None

    def __add__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(self.x + v, self.y + v, self.z + v)

    def __radd__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(self.x + v, self.y + v, self.z + v)

    def __sub__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(self.x - v, self.y - v, self.z - v)

    def __rsub__(self, v):
        if isinstance(v, Vector):
            return Vector(v.x - self.x, v.y - self.y, v.z - self.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(v - self.x, v - self.y, v - self.z)

    def __mul__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x * v.x, self.y * v.y, self.z * v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(self.x * v, self.y * v, self.z * v)

    def __rmul__(self, v):
        if isinstance(v, Vector):
            return Vector(v.x * self.x, v.y * self.y, v.z * self.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(v * self.x, v * self.y, v * self.z)

    def __truediv__(self, v):
        if isinstance(v, Vector):
            return Vector(self.x / v.x, self.y / v.y, self.z / v.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(self.x / v, self.y / v, self.z / v)

    def __rtruediv__(self, v):
        if isinstance(v, Vector):
            return Vector(v.x / self.x, v.y / self.y, v.z / self.z)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Vector(v / self.x, v / self.y, v / self.z)

    def __abs__(self):
        return Vector(np.abs(self.x), np.abs(self.y), np.abs(self.z))

    @staticmethod
    def real(v):
        return Vector(np.real(v.x), np.real(v.y), np.real(v.z))

    @staticmethod
    def imag(v):
        return Vector(np.imag(v.x), np.imag(v.y), np.imag(v.z))

    def yzx(self):
        return Vector(self.y, self.z, self.x)

    def xyz(self):
        return Vector(self.x, self.y, self.z)

    def zxy(self):
        return Vector(self.z, self.x, self.y)

    def average(self):
        return (self.x + self.y + self.z) / 3

    def matmul(self, matrix):
        if isinstance(self.x, numbers.Number):
            return array_to_vec3(np.dot(matrix, self.to_array()))
        elif isinstance(self.x, np.ndarray):
            return array_to_vec3(np.tensordot(matrix, self.to_array(), axes=([1, 0])))

    def change_basis(self, new_basis):
        return Vector(self.dot(new_basis[0]), self.dot(new_basis[1]), self.dot(new_basis[2]))

    def __pow__(self, a):
        return Vector(self.x ** a, self.y ** a, self.z ** a)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    @staticmethod
    def exp(v):
        return Vector(np.exp(v.x), np.exp(v.y), np.exp(v.z))

    @staticmethod
    def sqrt(v):
        return Vector(np.sqrt(v.x), np.sqrt(v.y), np.sqrt(v.z))

    def to_array(self):
        return np.array([self.x, self.y, self.z])

    def cross(self, v):
        return Vector(self.y * v.z - self.z * v.y, -self.x * v.z + self.z * v.x, self.x * v.y - self.y * v.x)

    def length(self):
        return np.sqrt(self.dot(self))

    def square_length(self):
        return self.dot(self)

    def normalize(self):
        mag = self.length()
        return self * (1.0 / np.where(mag == 0, 1, mag))

    def components(self):
        return self.x, self.y, self.z


    @staticmethod
    def random(_min_=0.,_max_=1.):
        return Vector(uniform(_min_, _max_),uniform(_min_,_max_),uniform(_min_,_max_))

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vector.random(-1,1)
            if p.square_length() >= 1:
                continue
            return p

    def extract(self, cond):
        return Vector(extract(cond, self.x),
                      extract(cond, self.y),
                      extract(cond, self.z))

    @staticmethod
    def where(cond, out_true, out_false):
        return Vector(np.where(cond, out_true.x, out_false.x),
                      np.where(cond, out_true.y, out_false.y),
                      np.where(cond, out_true.z, out_false.z))

    @staticmethod
    def select(mask_list, out_list):
        out_list_x = [i.x for i in out_list]
        out_list_y = [i.y for i in out_list]
        out_list_z = [i.z for i in out_list]

        return Vector(np.select(mask_list, out_list_x),
                      np.select(mask_list, out_list_y),
                      np.select(mask_list, out_list_z))

    def clip(self, min, max):
        return Vector(np.clip(self.x, min, max),
                      np.clip(self.y, min, max),
                      np.clip(self.z, min, max))

    def place(self, cond):
        r = Vector(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.x, cond, self.x)
        np.place(r.y, cond, self.y)
        np.place(r.z, cond, self.z)
        return r

    def repeat(self, n):
        return Vector(np.repeat(self.x, n), np.repeat(self.y, n), np.repeat(self.z, n))

    def reshape(self, *newshape):
        return Vector(self.x.reshape(*newshape), self.y.reshape(*newshape), self.z.reshape(*newshape))

    def shape(self, *newshape):
        if isinstance(self.x, numbers.Number):
            return 1
        elif isinstance(self.x, np.ndarray):
            return self.x.shape

    def mean(self, axis):
        return Vector(np.mean(self.x, axis=axis), np.mean(self.y, axis=axis), np.mean(self.z, axis=axis))

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y) & (self.z == other.z)


def array_to_vec3(array):
    return Vector(array[0], array[1], array[2])
