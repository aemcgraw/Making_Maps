from PIL import Image

from random import randint

from app.regions.Island import Island
from app.regions.Forest import Forest
from app.regions.Region import Region
from app.regions.Water import Water

import HeightMap

class Map(object):
    def __init__(self, heightmap, regionID, bound=None):
        self.image = image
        self.bounding_region = bound

        self.interior = set([])         #Unused, for compatibility with region
        self.edge = set([])             #Unused
        self.outer_edge = set([])       #Unused

        self.regionID = regionID
        self.regions = { x : [] for x in regionID.regionCount } # TODO : Define len() on regionID

    #def get_new_std_region(self, point):
    #    if point < 0:
    #        return Water(self.image)
    #    else:
    #        return Island(self.image)
    #
    #def get_region_from_point(self, point):
        

    def heightmap_to_regions(self, HeightMap):
        mapping = HeightMap.mapping
        
        init_point = mapping[0][0]
        new_region = self.get_new_std_region(init_point)
        new_region.edge.append(init_point)


    #def save(self, path):
    #    try:
    #        if not path.toLower().endswith('.png'):
    #            path += '.png'
    #        self.image.save(path, format='PNG')
    #    except IOError:
    #        print("Cannot convert")	
