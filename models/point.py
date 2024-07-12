from math import sqrt

class Point:
    x = None
    y = None

    def distance(self, other):
        return sqrt(
            (self.x - other.x)**2 + (self.y - other.y) ** 2
        )