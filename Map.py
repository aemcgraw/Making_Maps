from PIL import Image

from random import randint

from Island import Island
from Forest import Forest
from Region import Region

import HeightMap

class Map(Region):
    def __init__(self, image, bound=None):
        self.image = Image.new('RGBA', (image.width, image.height), (0, 0, 255, 255))
        self.bounding_region = bound

        self.interior = set([])         #Unused, for compatibility with region
        self.edge = set([])             #Unused
        self.outer_edge = set([])       #Unused

        self.islands = []
        self.forests = []

    def __init__(self, image, HeightMap, bound=None):
        self.image = HeightMap.image
        self.bounding_region = bound

        self.interior = set([])
        self.edge = set([])
        self.outer_edge = set([])

        self.islands = self.get_islands_from_heightmap(HeightMap)
        self.forests = []

    def get_islands_from_heightmap

    #Erases all islands
    def flood(self):
        self.image = Image.new('RGBA', (self.image.width, self.image.height), (0, 0, 255, 255))
        self.islands = []

    def draw_forest(self, count):
        island = self.islands[randint(0, len(self.islands) - 1)]
        new_forest = Forest(self.image, count, self, island)
        new_forest.build_forest()
        new_forest.add_forest_to_image()
        self.forests.append(new_forest)

    def draw_island(self, count):
        new_island = Island(self.image, count, self)
        new_island.build_island()
        new_island.add_island_to_image()
        new_island.add_shallows_to_image()
        self.islands.append(new_island)

    def draw_random_land(self, count):
        values_set = 0
        pixels = this.image.load()

        while values_set < count:
            new_x = randint(0, this.image.width - 1)
            new_y = randint(0, this.image.height - 1)
            pixels[new_x, new_y] = (0, 255, 0, 255)
            values_set += 1

    def get_weighted_seed(self):
        x = randint(0, 1)
        if ((x == 0) or (len(self.islands) == 0)):
            return self.get_seed()
        else:
            return self.get_some_closed_ext_point()

    #Gets a point on the outer_edge of a random region
    def get_some_closed_ext_point(self):
        if len(self.islands) == 0:
            return None
        some_ext = randint(0, len(self.islands) - 1)
        ext_point = self.islands[some_ext].get_closed_ext_point()
        return ext_point

    def save(self, path):
        try:
            if not path.toLower().endswith('.png'):
                path += '.png'
            self.image.save(path, format='PNG')
        except IOError:
            print("Cannot convert")	
