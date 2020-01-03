from PIL import Image

from random import randint
from random import uniform

import math

class HeightMap(object):
    def __init__(self, image):
        self.image = Image.new('RGBA', (image.width, image.height), (0, 0, 255, 255))
        self.scale = 1

        self.mapping = self._get_setup()

    def _get_setup(self):
        rows = []
        column = [0] * self.image.height
        for x in range(self.image.width):
            rows.append(column[:])
        return rows

    def fuzz(self):
        fuzzfactor = self.scale / 20
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                self.mapping[x][y] += (uniform(-fuzzfactor, fuzzfactor))

    def heightmap_to_image(self):
        pixels = self.image.load()

        print(max([max(x) for x in self.mapping]))
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
