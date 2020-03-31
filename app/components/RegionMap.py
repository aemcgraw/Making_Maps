from PIL import Image

from random import randint

from app.regions.rIsland import rIsland
from app.regions.rForest import rForest
from app.components.Region import Region
from app.regions.Water import Water

from app.components.HeightMap import HeightMap

class RegionMap(object):
    def __init__(self, image, heightmap, regionID, bound=None):
        self.image = image
        self.heightmap = heightmap

        self.regionID = regionID
        self.base_region = Region(image)
        self.regions = { x : [] for x in range(regionID.regioncount) }

        self.heightmap_to_regions()
        #self.color_regions()
        
    def get_region_from_point(self, point):
        (a, b) = point
        mapping = self.heightmap.mapping
        #print(str(point))
        ident = self.regionID.ident(mapping[a][b])
            
        new_region = self.regionID.get_new_region(mapping[a][b], self.image, bound=self.base_region)
        new_region.interior.add(point)
        rem_points = [ point ]

        while len(rem_points) > 0:
            (a, b) = rem_points.pop()
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    (c, d) = (a + x, b + y)
                    if (c, d) in self.base_region.interior:
                        if self.regionID.ident(mapping[c][d]) == ident:
                            if not (c, d) in new_region.interior:
                                #print(str((c, d)))
                                new_region.interior.add((c, d))
                                rem_points.append((c, d))
        self.regions[ident].append(new_region)

        print(str(len(new_region.interior)))
        #print(str(new_region.interior))
        return new_region

    def heightmap_to_regions(self):
        mapping = self.heightmap.mapping
 
        new_region = self.get_region_from_point((0, 0))
        #print(str(len(new_region.interior)))
        rem_region = self.base_region.interior.difference(new_region.interior)
        #print(str(rem_region))

        #print(str(len(rem_region)))
        while len(rem_region) > 0:
            new_point = rem_region.pop()
            new_region = self.get_region_from_point(new_point)
            #print(str(len(new_region.interior)))
            rem_region = rem_region.difference(new_region.interior)
            #print(str(len(rem_region)))

    def color_regions(self):
        for region_group in self.regions:
            for region in self.regions[region_group]:
                region.color()

    def outline_regions(self):
        for region_group in self.regions:
            for region in self.regions[region_group]:
                region.outline()

    #def save(self, path):
    #    try:
    #        if not path.toLower().endswith('.png'):
    #            path += '.png'
    #        self.image.save(path, format='PNG')
    #    except IOError:
    #        print("Cannot convert")	
