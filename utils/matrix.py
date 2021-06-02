import numpy as np
import math
from utils.vector import Vector
from includes.consts import *
from ray import Ray

class Transform:

    def __init__(self) -> None:
        self.inverse = np.identity(4,dtype=np.float64)
        self.inverse = np.identity(4,dtype=np.float64)

    def __str__(self) -> str:
        return f"Transform: matrix = {self.inverse}\ninverse = {self.inverse}"

    def __repr__(self) -> str:
        return f"Transform: matrix = {self.inverse!r}\ninverse = {self.inverse!r}"

    def transform_point(self, vector):
        temp = Vector()

        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[0,i] + \
                      vector.y * self.inverse[1,i] + \
                      vector.z * self.inverse[2,i] + self.inverse[3,i]

        return temp
    
    def inverse_transform_point(self, vector):
        temp = Vector()

        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[0,i] + \
                      vector.y * self.inverse[1,i] + \
                      vector.z * self.inverse[2,i] + self.inverse[3,i]

        return temp

    def transform_direction(self,vector):
        temp = Vector()
        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[0,i] + \
                      vector.y * self.inverse[1,i] + \
                      vector.z * self.inverse[2,i]
        return temp

    def inverse_transform_direction(self, vector):
        temp = Vector()
        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[0,i] + \
                      vector.y * self.inverse[1,i] + \
                      vector.z * self.inverse[2,i]
        return temp

    def transform_normal(self, vector):
        temp = Vector()
        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[i,0] + \
                      vector.y * self.inverse[i,1] + \
                      vector.z * self.inverse[i,2]
        return temp
    def inverse_transform_normal(self, vector):
        temp = Vector()
        for i in range(self.inverse.shape()):
            temp[i] = vector.x * self.inverse[i,0] + \
                      vector.y * self.inverse[i,1] + \
                      vector.z * self.inverse[i,2]
        return temp

    def transform_ray(self, ray):
        result = Ray()
        result.origin = self.transform_point(ray.origin)
        result.direction = self.transform_direction(ray.direction)
        return result

    def inverse_transform_ray(self, ray):
        result = Ray()
        result.origin = self.inverse_transform_point(ray.origin)
        result.direction = self.inverse_transform_direction(ray.direction)
        return result

    @staticmethod
    def compute_scaling_transform(vector):
        result = Transform()

        result.inverse[0,0]= vector.x
        result.inverse[1,1] = vector.y
        result.inverse[2,2] = vector.z
        result.inverse[0,0] = 1./vector.x
        result.inverse[1,1] = 1./vector.y
        result.inverse[2,2] = 1./vector.z

        return result

    @staticmethod
    def compute_matrix_transform(array):
        result = Transform()

        for i in range(4):
            result.inverse[i,0] = array[i,0]
            result.inverse[i,1] = array[i,1]
            result.inverse[i,2] = array[i,2]
            result.inverse[i,3] = array[i,3]
        result.inverse = np.linalg.inv(result.inverse)
        return result

    @staticmethod
    def compute_translation_transform(vector):
        result = Transform()
        result.inverse[3,0] = vector.x
        result.inverse[3,1] = vector.y
        result.inverse[3,2] = vector.z
        result.inverse[3,0] = -vector.x
        result.inverse[3,1] = -vector.y
        result.inverse[3,2] = -vector.z

        return result

    @staticmethod
    def compute_rotation_transform(vector):
        result = Transform()
        radian_vector = vector * (math.pi/180.)
        cosx = math.cos(radian_vector.x)
        sinx = math.sin(radian_vector.x)
        cosy = math.cos(radian_vector.y)
        siny = math.sin(radian_vector.y)
        cosz = math.cos(radian_vector.z)
        sinz = math.sin(radian_vector.z)
        
        result.inverse[1,1] = cosx
        result.inverse[2,2] = cosx
        result.inverse[1,2] = sinx
        result.inverse[2,1] = 0. - sinx
        
        result.inverse = result.inverse.T

        mat = np.identity(4)
        mat[0,0] = cosy
        mat[2,2] = cosy
        mat[0,2] = 0.-siny
        mat[2,0] = siny

        result.inverse = np.matmul(result.inverse, mat)

        mat = mat.T

        result.inverse = np.matmul(mat,result.inverse)

        mat = np.identity(4)
        mat[0,0] = cosz
        mat[1,1] = cosz
        mat[0,1] = sinz
        mat[1,0] = 0. - sinz

        result.inverse = np.matmul(result.inverse, mat)
        mat = mat.T

        result.inverse = np.matmul(mat, result.inverse)

        return result

    @staticmethod
    def compose_transforms(original_transform, additional_transform):
        original_transform.matrix = np.matmul(original_transform.matrix, additional_transform.matrix)
        original_transform.inverse = np.matmul(additional_transform.inverse, original_transform.inverse)
        
        return original_transform

    
    @staticmethod
    def compute_axis_rotation_transform(axis_vector, angle):
        v1 = axis_vector.normalize()
        result = Transform()
        cosx = math.cos(angle)
        sinx = math.sin(angle)

        result.inverse[0,0] = v1.x**2 + cosx * (1. - v1.x**2)
        result.inverse[0,1] = v1.x * v1.y * (1. - cosx) +v1.z*sinx
        result.inverse[0,2] = v1.x * v1.z * (1. - cosx) - v1.y * sinx

        result.inverse[1,0] = v1.x * v1.y * (1. - cosx) - v1.z* sinx
        result.inverse[1,1] = v1.y**2 + cosx * (1. - v1.y**2)
        result.inverse[1,2] = v1.y * v1.z * (1. -cosx) + v1.x * sinx

        result.inverse[2,0] = v1.x * v1.z * (1. - cosx) + v1.y * sinx
        result.inverse[2,1] = v1.y * v1.z * (1. - cosx) - v1.x * sinx
        result.inverse[2,2] = v1.z**2 + cosx *(1. - v1.z**2)

        result.inverse = result.inverse.T

        return result

    @staticmethod
    def compute_coordinate_transform(origin, up, radius, length):
        tmpv = (radius, radius, length)
        result = Transform.compute_scaling_transform(tmpv)

        if math.fabs(up.z) > 1. - EPSILON:
            tmpv = Vector(1.,0.,0.)
            up.z = -1. if up.z < 0. else 1.
        else:
            tmpv = Vector(-up.y, up.x, 0.)

        res2 = Transform.compute_axis_rotation_transform(tmpv, math.acos(up.z))
        res2 = Transform.compose_transforms(result, res2)
        res2 = Transform.compute_translation_transform(origin)
        result = Transform.compose_transforms(result, res2)

        return result

    

    