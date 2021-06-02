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

from abc import abstractclassmethod
from utils.vector import Vector
from ray import Ray


class Camera:
    """Basic camera """

    # TODO: add focal blur items
    def __init__(self, location=Vector(0, 0, 0), direction=Vector(0, 0, 1), up=Vector(0, 1, 0),
                 right=Vector(1.33, 0.0, 0.0),
                 sky=Vector(0, 1, 0), look_at=Vector(0, 0, 1), focal_point=Vector(0, 0, 1), viewing_angle=90):
        self.location = location
        self.direction = direction
        self.up = up
        self.right = right
        self.sky = sky
        self.look_at = look_at
        self.focal_point = focal_point
        self.viewing_angle = viewing_angle  # angle

    def setup_camera(self):
        # aspect_ratio = 4./3.
        # camera_dir = self.direction
        # camera_right = self.right
        # camera_loc = self.location
        # camera_up = self.up
        camera_len_right = self.right.length()
        camera_len_up = self.up.length()

        return camera_len_right / camera_len_up

    @abstractclassmethod
    def create_camera_ray(self, x, y, width, height, ray_no):
        pass


class PerspectiveCamera(Camera):
    """ A standard pin-hole camera """
    def create_camera_ray(self, x, y, width, height, ray_no):
        ray = Ray(self.location)
        x0 = x/width -0.5
        y0 = 0.5 - y/height 
        ray.direction = self.direction + x0 * self.right + y0 * self.up
        ray.direction = ray.direction.normalize()

        return ray
