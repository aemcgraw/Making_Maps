from PIL import Image

from random import randint

class Region(object):
    def __init__(self, image, bound=None):
        self.image = image
        self.bounding_region = bound    #Reference to an exterior region fully containing this region

        self.interior = set([])
        self.edge = set([]) #Not getting set anywhere
        self.outer_edge = set([])

        if bound == None:
            for x in range(self.image.width):
                for y in range(self.image.height):
                    self.interior.add((x, y))

#    def __init__(self, image, interior, bound=None):
#        self.image = image
#        self.bounding_region = bound

#        self.interior = interior
#        self.edge = set([])
#        self.outer_edge([])

    #All points in the region
    def get_interior(self):
        return self.interior

    #All points in the region which are adjacent to a point outside it
    def get_edge(self):
        if len(self.edge) == 0:
            self.calculate_edge()
        return self.edge

    #All points not in the region which are adjacent to a point inside it
    def get_outer_edge(self):
        if len(self.outer_edge) == 0:
            self.calculate_outer_edge()
        return self.interior

    def get_interior_point(self):
        point = self.interior.pop()
        self.interior.add(point)
        return point

    def get_edge_point(self):
        point = self.edge.pop()
        self.edge.add(point)
        return point

    def get_outer_edge_point(self):
        point = self.outer_edge.pop()
        self.outer_edge.add(point)
        return point

    def calculate_edge(self):
        for (a, b) in self.interior:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    point = (a + i, b + j)
                    if point not in self.interior:
                        self.edge.add( (a, b) )

    def calculate_outer_edge(self):
        for (a, b) in self.edge:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    point = (a + i, b + j)
                    if point not in self.interior:
                        self.outer_edge.add(point) 

    def difference(self):
        return self.bounding_region.interior.difference(self.interior)

    def outline(self):
        pixels = self.image.load()
        interior = self.get_interior()
        for (x, y) in interior:
            pixels[x, y] = (255, 255, 255, 255)
        edge = self.get_edge()
        for (x, y) in edge:
            pixels[x, y] = (0, 0, 0, 255)

    def get_seed(self):
        if self.bounding_region != None and len(self.bounding_region.interior) != 0:
            return self.bounding_region.get_interior_point()
        else:
            return (randint(0, self.image.width - 1), randint(0, self.image.height - 1))
