from vector import Vector

class BoundingBox:

    def __init__(self, llx, lly, llz,lex,ley,lez):
        self.lowerleft = Vector(llx,lly,llz)
        self.size = Vector(lex,ley,lez)

    def get_max(self):
        return self.lowerleft + self.size

    def is_empty(self):
        return self.size.x < 0. or self.size.y < 0. or self.size.z < 0.

    def inside(self, point):
        if point.x < self.lowerleft.x:
            return False
        if point.y < self.lowerleft.y:
            return False
        if point.z < self.lowerleft.z:
            return False
        if point.x > self.lowerleft.x + self.size.x:
            return False
        if point.y > self.lowerleft.y + self.size.y:
            return False
        if point.z > self.lowerleft.z + self.size.z:
            return False
        return True
    
    def bounds_volume(self, a):
        return self.size.x * self.size.y * self.size.z
        