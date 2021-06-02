import numpy as np
import numbers

def extract(cond, x):
    if isinstance(x, numbers.Number):
        return x
    else:
        return np.extract(cond, x)

class Color:
    
    def __init__(self, x, y, z):
        self.red = x
        self.green = y
        self.blue = z
    
    def __str__(self):
        # Used for debugging. This method is called when you print an instance  
        return "(" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"

             
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
            return Color(v.red - self.red, v.green - self.green ,  v.blue - self.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v  - self.red, v  - self.green ,  v - self.blue)

    def __mul__(self, v):
        if isinstance(v, Color):
            return Color(self.red * v.red , self.green *  v.green , self.blue * v.blue )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red * v, self.green * v, self.blue * v) 
    def __rmul__(self, v):
        if isinstance(v, Color):
            return Color(v.red *self.red  , v.green * self.green, v.blue * self.blue )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v *self.red  , v * self.green, v * self.blue ) 
    def __truediv__(self, v):
        if isinstance(v, Color):
            return Color(self.red / v.red , self.green /  v.green , self.blue / v.blue )
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(self.red / v, self.green / v, self.blue / v)


    def __rtruediv__(self, v):
        if isinstance(v, Color):
            return Color(v.red / self.red, v.green / self.green, v.blue / self.blue)
        elif isinstance(v, numbers.Number) or isinstance(v, np.ndarray):
            return Color(v / self.red, v / self.green, v / self.blue)
    

    
    def __abs__(self):
        return Color(np.abs(self.red), np.abs(self.green), np.abs(self.blue))
    
    def real(v):
        return Color(np.real(v.red), np.real(v.green), np.real(v.blue))
    
    def imag(v):
        return Color(np.imag(v.red), np.imag(v.green), np.imag(v.blue))  

    def yzx(self):
        return Color(self.green, self.blue, self.red)  
    def xyz(self):
        return Color(self.red, self.green, self.blue)
    def zxy(self):
        return Color(self.blue, self.red, self.green)
    def xyz(self):
        return Color(self.red, self.green, self.blue)  


    def average(self):
        return (self.red + self.green +  self.blue)/3
    
    def matmul(self, matrix):
        if isinstance(self.red, numbers.Number):
            return array_to_vec3(np.dot(matrix,self.to_array()))
        elif isinstance(self.red, np.ndarray):
            return array_to_vec3(np.tensordot(matrix,self.to_array() , axes=([1,0])))

    def change_basis(self, new_basis):
        return Color(self.dot(new_basis[0]),  self.dot(new_basis[1]),   self.dot(new_basis[2]))

    def __pow__(self, a):
        return Color(self.red**a, self.green**a, self.blue**a)
    
    def dot(self, v):
        return self.red*v.x + self.green*v.y + self.blue*v.z
    
    def exp(v):
        return Color(np.exp(v.red) , np.exp(v.green) ,np.exp(v.blue))
    
    def sqrt(v):
        return Color(np.sqrt(v.red) , np.sqrt(v.green) ,np.sqrt(v.blue)) 
    
    def to_array(self):
        return np.array([self.red , self.green , self.blue])

    def cross(self, v):
        return Color(self.green*v.z - self.blue*v.y, -self.red*v.z + self.blue*v.x,  self.red*v.y - self.green*v.x)
    
    def length(self):
        return np.sqrt(self.dot(self))
    
    def square_length(self):
        return self.dot(self)

    def normalize(self):
        mag = self.length()
        return self * (1.0 / np.where(mag == 0, 1, mag))
 


    def components(self):
        return (self.red, self.green, self.blue)
    
    def extract(self, cond):
        return Color(extract(cond, self.red),
                    extract(cond, self.green),
                    extract(cond, self.blue))

    def where(self, cond, out_true, out_false):
        return Color(np.where(cond, out_true.red, out_false.red),
                    np.where(cond, out_true.green, out_false.green),
                    np.where(cond, out_true.blue, out_false.blue))

    def select(self, mask_list, out_list):
        out_list_x = [i.x for i in out_list]
        out_list_y = [i.y for i in out_list]
        out_list_z = [i.z for i in out_list]

        return Color(np.select(mask_list, out_list_x),
                    np.select(mask_list, out_list_y),
                    np.select(mask_list, out_list_z))

    def clip(self, min, max):
        return Color(np.clip(self.red, min, max),
                    np.clip(self.green, min, max),
                    np.clip(self.blue, min, max))

    def place(self, cond):
        r = Color(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.red, cond, self.red)
        np.place(r.green, cond, self.green)
        np.place(r.blue, cond, self.blue)
        return r

    def repeat(self, n):
        return Color(np.repeat(self.red , n), np.repeat(self.green , n),   np.repeat(self.blue , n))

    def reshape(self, *newshape):
        return Color(self.red.reshape(*newshape), self.green.reshape(*newshape),   self.blue.reshape(*newshape))

    def shape(self, *newshape):
        if isinstance(self.red, numbers.Number):
            return 1
        elif isinstance(self.red, np.ndarray):
                return self.red.shape

    def mean(self, axis):
        return Color(np.mean(self.red,axis = axis), np.mean(self.green,axis = axis),   np.mean(self.blue,axis = axis))

    def __eq__(self, other):
        return (self.red == other.x)  &  (self.green == other.y) & (self.blue == other.z)

    
    def array_to_vec3(self, array):
        return Color(array[0],array[1],array[2])

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)


class Colors:
    Black = Color(0.,0.,0.)
    White = Color(1.,1.,1.)
    Red = Color(1.,0.,0.)
    Green = Color(0.,1.,0.)
    Blue = Color(0.,0.,1.)

    