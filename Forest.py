from PIL import Image

from random import randint

from Region import Region

class Forest(Region):
    def __init__(self, image, count, map, island):
        self.image = image
        self.map = map
        self.bounding_region = island
        seed = self.get_seed()

        self.interior = set([seed])
        self.edge = set([])
        self.outer_edge = set([])
        self.count = count

        self.add_shallows(seed)

    #TODO : This method looks really expensive
    def add_shallows(self, location):
        (x_loc, y_loc) = location
        for x_adjust in range(-1, 2, 1):
            for y_adjust in range(-1, 2, 1):
                potential_point = (x_loc + x_adjust, y_loc + y_adjust)
                if (self._is_valid(potential_point) and (potential_point not in self.interior) and 
                                                (potential_point in self.bounding_region.interior)):
                    self.outer_edge.add(potential_point)

    def add_land_random(self):
        if len(self.outer_edge) != 0:
            #random_position = randint(0, len(self.shallows) - 1)
            #new_land = self.shallows.pop(random_position)

            new_land = self.outer_edge.pop()
            #This might not be very random
            self.interior.add(new_land)
            self.add_shallows(new_land)

    def _is_valid(self, point):
        (x, y) = point
        if x >= 0 and y >= 0 and x < (self.image.width) and y < (self.image.height):
            return True
        return False

    def build_forest(self):
        i = 0
        while i < self.count:
            self.add_land_random()
            i+=1

    def add_forest_to_image(self):
        pixels = self.image.load()
        for (land_x, land_y) in self.interior:
            pixels[land_x, land_y] = (0, 128, 64, 255)
