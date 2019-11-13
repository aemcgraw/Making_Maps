from PIL import Image

from random import randint

class Region():
    def __init__(self, image, bound=None):
        self.image = image
        self.bounding_region = bound
        self.interior = set([])
        self.open_exterior = set([])
        self.closed_exterior = set([])

    def calculate_closed_exterior(self):
        for (a, b) in self.open_exterior:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    point = (a + i, b + j)
                    if point not in self.interior:
                        self.closed_exterior.add(point) 

    def get_closed_exterior(self):
        if len(self.closed_exterior) == 0:
            self.calculate_closed_exterior()
        return self.interior

    def get_open_ext(self):
        return self.open_exterior

    def get_interior(self):
        return self.interior

    def get_closed_ext_point(self):
        point = self.closed_exterior.pop()
        self.closed_exterior.add(point)
        return point

    def get_open_ext_point(self):
        point = self.open_exterior.pop()
        self.open_exterior.add(point)
        return point

    def get_interior_point(self):
        point = self.interior.pop()
        self.interior.add(point)
        return point

    def get_seed(self):
        if self.bounding_region != None and len(self.bounding_region.interior) != 0:
            return self.bounding_region.get_interior_point()
        else:
            return (randint(0, self.image.width - 1), randint(0, self.image.height - 1))
