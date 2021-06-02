#  MIT License
#
#  Copyright (c) [year] [fullname]
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

#  MIT License
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
from math import sqrt
import math
from material import Material
from matrix import Transform
from ray import Ray
import numpy as np
from utils.vector import Vector
from utils.boundingbox import BoundingBox

class Sphere:
    """Sphere is the only 3D shape implemented. Has center, radius and material"""

    def __init__(self, center: Vector, radius, material: Material,do_ellipsoid=False):
        self.center = center
        self.radius = radius
        self.material = material
        self.transform_matrix = None
        self.do_ellispoid = do_ellipsoid

    def intersects(self, ray: Ray):
        """Checks if ray intersects this sphere. Returns distance to intersection or None if there is no intersection"""
        b = 2 * np.dot(ray.direction, ray.origin - self.center)
        c = np.linalg.norm(ray.origin - self.center) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
        return None

    def normal(self, ipoint:Vector):
        """Returns surface normal to the point on sphere's surface"""
        if self.do_ellispoid:
            newpoint = self.transform_matrix.inverse_transform_point(ipoint)
            result = newpoint
            result = self.transform_matrix.transform_normal(result)
            result = result.normalize()
        else:
            result = (ipoint - self.center) * (1./self.radius)
        return result

    def inside(self, ipoint):
        if self.do_ellispoid:
            newpoint = self.transform_matrix.invervse_transform_point(ipoint)
            ocsqr = newpoint.square_length()
            return ocsqr < (self.radius**2)
        else:
            origin_to_center = self.center - ipoint
            ocsqr = origin_to_center.length()**2
            return ocsqr < self.radius**2

    def translate(self, vector):
        if self.do_ellispoid:
            self.transform()

        else:

          self.center += vector
          self.compute_bounding_box()

    def transform(self):
        if not self.do_ellispoid:
            self.do_ellispoid = True
            if self.transform_matrix is None:
                self.transform_matrix = Transform()
            temp = Transform()
            temp = Transform.compute_scaling_transform(Vector(self.radius, self.radius,self.radius))
            self.transform_matrix = Transform.compose_transforms(self.transform_matrix,temp)
            self.radius = 1.
            temp = Transform.compute_translation_transform(self.center)
            self.transform_matrix = Transform.compose_transforms(self.transform_matrix, temp)
            self.center = Vector(0.,0.,0.)
        self.transform_matrix = Transform.compose_transforms(self.transform_matrix)
        self.compute_bounding_box()
    
    def scale(self, vector):
        self.center *= vector.x
        self.radius *= math.fabs(vector.x)
        self.compute_bounding_box()

    def compute_bounding_box(self):
        self.bounding_box = BoundingBox(self.center.x - self.radius, self.center.y - self.radius, 
                                        self.center.z-self.radius,2 * self.radius,2 * self.radius,2 * self.radius)

    def uv_coordinates(self, ipoint):
        M_C = (ipoint - self.center) / self.radius
        phi = np.arctan2(M_C.z, M_C.x)
        theta = np.arcsin(M_C.y)
        u = (phi + np.pi) / (2*np.pi)
        v = (theta + np.pi/2) / np.pi
        return u,v

    def intersect_bounding_box(self):
        return True

    def rotate(self, trans):
        if self.do_ellispoid:
            self.transform()
        else:
            if self.transform_matrix is None:
                self.transform_matrix = Transform()
            self.transform_matrix = Transform.compose_transforms(self.transform_matrix,trans)
            self.center = Transform.transform_point(self.center)
            self.compute_bounding_box()

        # u = u.normalize()
        # θ = θ/180 *np.pi 
        # cosθ = np.cos(θ)
        # sinθ = np.sqrt(1-cosθ**2) * np.sign(θ)
        
        # #rotation matrix along u axis
        # M = np.array([
        #                [cosθ + u.x*u.x * (1-cosθ),      u.x*u.y*(1-cosθ) - u.z*sinθ,         u.x*u.z*(1-cosθ) +u.y*sinθ],
        #                [u.y*u.x*(1-cosθ) + u.z*sinθ,        cosθ + u.y**2 * (1-cosθ),       u.y*u.z*(1-cosθ) -u.x*sinθ],
        #                [u.z*u.x*(1-cosθ) -u.y*sinθ,             u.z*u.y*(1-cosθ) + u.x*sinθ,         cosθ + u.z*u.z*(1-cosθ)]
        #               ])
