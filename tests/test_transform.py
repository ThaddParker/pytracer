import unittest
from utils.vector import Vector
from utils.matrix import Transform
import numpy as np

class Test_Transform(unittest.TestCase):

    def test_compute_rotation_transform(self):
        vec = Vector(1,2,3)

        result = Transform.compute_rotation_transform(vec)

        print(vec)
        print(result)

    def test_compute_scaling_transform(self):
        vec = Vector(1,2,3)
        result = Transform.compute_scaling_transform(vec)

        print(vec)
        print(result)

    def test_compute_matrix_transform(self):
        mat = np.array([[1.,2.,3.,3],[2.,3.,3.,1.],[3.,3.,1.,2.],[3.,1.,2.,3.]])
        result = Transform.compute_matrix_transform(mat)

        print(mat)
        print(result)

    def test_compute_translation_transform(self):
        vec = Vector(1,2,3)
        result = Transform.compute_translation_transform(vec)

        print(vec)
        print(result)

    
