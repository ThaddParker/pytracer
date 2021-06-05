#  MIT License
#
#  Copyright (c) 2021 [fullname]
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

from abc import abstractmethod
from utils.vector import Vector
from ray import Ray


class Camera:
    """Basic camera """

    # TODO: add focal blur items
    def __init__(self, **kwargs):
        self.location = kwargs.get('location', Vector())
        self.direction = kwargs.get('direction', Vector(z=1.))
        self.up = kwargs.get('up', Vector(y=1.))
        self.right = kwargs.get('right', Vector(x=1.33)) # this is for left handed viewing
        self.sky = kwargs.get('sky', Vector(y=1)) # y is positive up
        self.look_at = kwargs.get('look_at', Vector(z=1.)) # z is positive into the screen
        self.focal_point = kwargs.get('focal_point', Vector(z=1.0))
        self.viewing_angle = kwargs.get('viewing_angle', 90.)   # angle 90 degrees from lens?
        self.type = "Base Camera"
        self.aspect_ratio = self.right.length() / self.up.length()

        # other items
        self.aspect_ratio = 16. / 9.
        self.image_width = 400
        self.image_height = int(self.image_width / self.aspect_ratio)

        self.viewport_height = 2.
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.

        # camera
        origin = Vector()
        self.horizontal = Vector(self.viewport_width, 0, 0)
        self.vertical = Vector(0, self.viewport_height, 0)
        self.lower_left_corner = origin - self.horizontal / 2 - self.vertical / 2 - Vector(0, 0, self.focal_length)

    @abstractmethod
    def create_camera_ray(self, x, y):
        return Ray(self.location, self.lower_left_corner + x * self.horizontal + y * self.vertical - self.location)


class PerspectiveCamera(Camera):
    """ A standard pin-hole camera """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().type = "Perspective Camera"

    def create_camera_ray(self, x, y, width, height, ray_no):
        ray = Ray(self.location, Vector())
        x0 = x / width - 0.5
        y0 = 0.5 - y / height
        ray.direction = self.direction + x0 * self.right + y0 * self.up
        ray.direction = ray.direction.normalize()

        return ray

