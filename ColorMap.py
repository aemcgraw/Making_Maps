from PIL import Image

from HeightMap import HeightMap

import math

class ColorMap():
    def __init__(self, image, heightmap):
        self.image = image
        self.heightmap = heightmap
        self.mapping = heightmap.mapping
        self.scale = heightmap.scale

    def greyscale(self):
        pixels = self.image.load()

        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y] + 1
                pixels[x, y] = ( int(127 * val),
                                 int(127 * val),
                                 int(127 * val),
                                 255 )

    def forest_nothing(self):
        pixels = self.image.load()

        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                if self.mapping[x][y] > 0:
                    pixels[x, y] = (0, 128, 0, 255)

    def std(self):
        pixels = self.image.load()

        print(max([max(x) for x in self.mapping]))
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y]
                if val < 0:
                    sc = max(1 + (val / 3), 0.5)
                    #pixels[x, y] = (80, int(180 - math.sqrt(-val) * 100), 255, 255)
                    #TODO : Find a better expression to evaluate this
                    pixels[x, y] = (int(sc * 80), int( (180 - math.sqrt(-val) * 100) * sc), int(sc * 255), 255)
                elif val/self.scale > 0.7:
                    pixels[x, y] = (255, 255, 255, 255)
                elif val/self.scale > 0.3:
                    pixels[x, y] = (120, 120, 120, 255)
                else:
                    pixels[x, y] = (int(120 * val / self.scale),
                                        max(120, 255-int(135 * val / self.scale)),
                                        int(120 * val / self.scale), 255)

    def cosmic(self):
        pixels = self.image.load()

        print(max([max(x) for x in self.mapping]))
        print("COSMIC")
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                val = self.mapping[x][y]
                if val/self.scale < 0:
                    pixels[x, y] = (0, 0, 0, 255)
                else:
                    pixels[x, y] = (0, 255, 0, 255)
