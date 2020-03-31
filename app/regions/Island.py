from PIL import Image

from random import randint

from app.components.Region import Region

class Island(Region):
    def __init__(self, image, bound=None):
        super().__init__(image, bound=bound)

    def __init__(self, image, size, map):
        self.image = image
        self.map = map
        self.bounding_region = map

        seed = map.get_weighted_seed()
        self.interior = set([ seed ])
        self.edge = set([])
        self.outer_edge = set([])
        self.size = size

        self.add_shallows(seed)

    def color():
        pixels = self.image.load
        for (x, y) in self.interior:
            pixels[x, y] = (0, 255, 0, 255)

    def add_shallows(self, location):
        (x_loc, y_loc) = location
        for x_adjust in range(-1, 2, 1):
            for y_adjust in range(-1, 2, 1):
                potential_point = (x_loc + x_adjust, y_loc + y_adjust)
                if self._is_valid(potential_point) and potential_point not in self.interior:
                    self.outer_edge.add(potential_point)

    def add_land_random(self):
        if len(self.outer_edge) != 0:
            #random_position = randint(0, len(self.shallows) - 1)
            #new_land = self.shallows.pop(random_position)

            new_land = self.outer_edge.pop()
            #This might not be very random
            self.interior.add(new_land)
            self.add_shallows(new_land)

    #TODO : Check against bounding region
    def _is_valid(self, point):
        (x, y) = point
        if x >= 0 and y >= 0 and x < (self.image.width) and y < (self.image.height):
            return True
        return False

    def build_island(self):
        i = 0
        while i < self.size:
            self.add_land_random()
            i+=1

    def add_island_to_image(self):
        pixels = self.image.load()
        for (land_x, land_y) in self.interior:
            pixels[land_x, land_y] = (0, 255, 0, 255)

    def add_shallows_to_image(self):
        pixels = self.image.load()
        for (shallow_x, shallow_y) in self.outer_edge:
            pixels[shallow_x, shallow_y] = (0, 255, 255, 255)
