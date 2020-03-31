#Function which takes a point in 2D space and assigns it to a region

from app.regions.rIsland import rIsland
from app.regions.Water import Water
from app.regions.rForest import rForest

class RegionID(object):
    def __init__(self):
        self.regioncount = 0

    def same_region(self, a, b):
        if self.ident(a) == self.ident(b):
            return True
        return False

class RegionID_std(RegionID):
    def __init__(self):
        self.regioncount = 2

class RegionID_forest(RegionID):
    def __init__(self):
        self.regioncount = 2

    def get_new_region(self, point, image, bound=None):
        if point < 0:
            return Water(image, bound=bound)
        else:
            return rForest(image, bound=bound)

    def ident(self, point):
        if point < 0:
            return 0
        else:
            return 1
