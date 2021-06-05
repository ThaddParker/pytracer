from utils.vector import Vector
from includes.consts import *


class BoundingBox:

    def __init__(self, llx=0., lly=0., llz=0., lex=0., ley=0., lez=0.):
        self.lower_left = Vector(llx, lly, llz)
        self.size = Vector(lex, ley, lez)

    def __str__(self):
        return f"{self.lower_left!s}\n{self.size!s}"

    def __repr__(self):
        return f"BoundingBox:\n  {self.lower_left!r}\n  {self.size!r}"

    def get_maxs(self):
        return self.lower_left + self.size

    def get_mins(self):
        return self.lower_left

    def is_empty(self):
        return self.size.x < 0. or self.size.y < 0. or self.size.z < 0.

    def inside(self, point):
        if point.x < self.lower_left.x or point.x > self.lower_left.x + self.size.x:
            return False
        if point.y < self.lower_left.y or point.y > self.lower_left.y + self.size.y:
            return False
        if point.z < self.lower_left.z or point.z > self.lower_left.z + self.size.z:
            return False
        # if ipoint.x > self.lower_left.x + self.size.x:
        #     return False
        # if ipoint.y > self.lower_left.y + self.size.y:
        #     return False
        # if ipoint.z > self.lower_left.z + self.size.z:
        #     return False
        return True

    def bounds_volume(self):
        return self.size.x * self.size.y * self.size.z

    def recompute_bounding_box(self, trans):
        if trans is None:
            return
        lleft = self.lower_left
        lens = self.size
        mins = Vector(BOUND_HUGE, BOUND_HUGE, BOUND_HUGE)
        maxs = Vector(-BOUND_HUGE, -BOUND_HUGE, -BOUND_HUGE)

        for i in range(1, 8):
            corner = lleft

            corner.x += lens.x if i & 1 else 0.0
            corner.y += lens.y if i & 2 else 0.0
            corner.z += lens.z if i & 4 else 0.0

            corner = trans.transform_point(corner)
            if corner.x < mins.x:
                mins.x = corner.x
            if corner.x > maxs.x:
                maxs.x = corner.x
            if corner.y < mins.y:
                mins.y = corner.y
            if corner.y > maxs.y:
                maxs.y = corner.y
            if corner.z < mins.z:
                mins.z = corner.z
            if corner.z > maxs.z:
                maxs.z = corner.z

        # clip bounding box
        if mins.x < -BOUND_HUGE / 2.:
            mins.x = -BOUND_HUGE / 2.
        if mins.y < -BOUND_HUGE / 2.:
            mins.y = -BOUND_HUGE / 2.
        if mins.z < -BOUND_HUGE / 2.:
            mins.z = -BOUND_HUGE / 2.
        if maxs.x > BOUND_HUGE / 2.:
            maxs.x = BOUND_HUGE / 2.
        if maxs.y > BOUND_HUGE / 2.:
            maxs.y = BOUND_HUGE / 2.
        if maxs.z > BOUND_HUGE / 2.:
            maxs.z = BOUND_HUGE / 2.

        self.lower_left = mins
        self.size = maxs - mins
