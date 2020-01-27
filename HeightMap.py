from PIL import Image

from random import randint
from random import uniform

import math
from statistics import median_low

class HeightMap(object):
    def __init__(self, image):
        self.image = image
        self.scale = 1

        self.mapping = self._get_setup()

    def _get_setup(self):
        rows = []
        column = [0] * self.image.height
        for x in range(self.image.width):
            rows.append(column[:])
        return rows

    def get_perc_above_0(self): #float
        val = 0
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                if self.mapping[x][y] > 0:
                    val += 1
        return val / ((self.image.width - 1) * (self.image.height - 1)) 

    def get_low_median(self): #flloat
        flatten_mapping = [ x for y in self.mapping for x in y ]
        quantiles = median_low(flatten_mapping)
        return quantiles

    #def get_quantiles(self): #[ float ]
    #    flatten_mapping = [ x for y in self.mapping for x in y ]
    #    quantiles = statistics.quantiles(flatten_mapping, n=10)
    #    return quantiles

    def adjust_global(self, adjust):
        adjust = round(adjust, 3)
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                self.mapping[x][y] -= adjust

    def erode(self):
        count = 0
        erosionthresh = 0.1
        ev = erosionthresh / 2
        for x in range(1, len(self.mapping) - 1):
            for y in range(1, len(self.mapping[x]) - 1):
                position = self.mapping[x][y]
                if position - self.mapping[x+1][y] > erosionthresh:
                    self.mapping[x][y] -= ev
                    self.mapping[x+1][y] += ev
                    count += 1
                if position - self.mapping[x][y+1] > erosionthresh:
                    self.mapping[x][y] -= ev
                    self.mapping[x][y+1] += ev
                    count += 1
                if position - self.mapping[x-1][y] > erosionthresh:
                    self.mapping[x][y] -= ev
                    self.mapping[x-1][y] += ev
                    count += 1
                if position - self.mapping[x][y-1] > erosionthresh:
                    self.mapping[x][y] -= ev
                    self.mapping[x][y-1] += ev
                    count += 1
        print("Eroded " + str(count) + " times")

    def fuzz(self):
        fuzzfactor = self.scale / 20
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                self.mapping[x][y] += (uniform(-fuzzfactor, fuzzfactor))

    def heightmap_to_image(self):
        pixels = self.image.load()

        print("MaxHeight : " + str(max([max(x) for x in self.mapping])))
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y]
                if val < 0:
                    pixels[x, y] = (0, 0, 255, 255)
                elif val/self.scale > 0.8:
                    pixels[x, y] = (255, 0, 0, 255)
                elif val/self.scale > 0.5:
                    pixels[x, y] = (255, 255, 255, 255)
                elif val/self.scale > 0.2:
                    pixels[x, y] = (120, 120, 120, 255)
                else:
                    pixels[x, y] = (int(120 * val / self.scale), 
                                        max(120, 255-int(135 * val / self.scale)),                                                         
                                        int(120 * val / self.scale), 255)

    def add(self, heightmap2):
        if (self.image.width != heightmap2.image.width or
                self.image.height != heightmap2.image.height or
                len(self.mapping) != len(heightmap2.mapping) or
                len(self.mapping[0]) != len(heightmap2.mapping[0])):
            print("Could not add heightmaps, dimensions did not match")
            return
        else:
            self.scale += heightmap2.scale
            print(str(self.scale))
            for x in range(len(self.mapping)):
                for y in range(len(self.mapping[x])):
                    self.mapping[x][y] += heightmap2.mapping[x][y]
