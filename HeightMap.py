from PIL import Image

from random import randint
from random import uniform

import math

class HeightMap():
    def __init__(self, image, scale=180, pointdist=10):
        self.image = Image.new('RGBA', (image.width, image.height), (0, 0, 255, 255))
        self.scale = (math.sqrt(2) / 2) * pointdist

        self.pointdist = pointdist
        self.grid_points =  self._get_grid_points()
        self.mapping = self._get_setup() 
        self.build_mapping()

    def _get_setup(self):
        rows = []
        column = [0] * self.image.height
        for x in range(self.image.width):
            rows.append(column[:])
        return rows

    def _get_rand_vector(self):
        radian = uniform(0, 6.28)
        x = math.cos(radian)
        y = math.sin(radian)
        return (x, y)

    def _get_grid_points(self):
        xpoints = range(0, self.image.width + self.pointdist, self.pointdist)
        ypoints = range(0, self.image.height + self.pointdist, self.pointdist)
        rows = []
        for x in range(len(xpoints)):
            column = [ self._get_rand_vector() for y in range(len(ypoints)) ]
            rows.append(column)

        for y in range(len(rows[0])):
            rows[-1][y] = rows[0][y]

        return rows       

    def _get_grid_index(self, x, y):
        xgrid = int(x / self.pointdist)
        ygrid = int(y / self.pointdist)
        return (xgrid, ygrid)

    def lerp(self, a0, a1, w):
        return (1.0 - w) * a0 + (w * a1)

    def dotGridGradient(self, a, b, x, y):
        ix = a * self.pointdist
        iy = b * self.pointdist

        #dx = (float(x) - ix) / self.pointdist
        #dy = (float(y) - iy) / self.pointdist
        dx = (float(x) - ix)
        dy = (float(y) - iy)

        gradient = (dx * self.grid_points[a][b][0]) + (dy * self.grid_points[a][b][1])

        return gradient

    def perlin(self, x, y):
        (a, b) = self._get_grid_index(x, y)
        x0 = a * self.pointdist
        x1 = (a + 1) * self.pointdist
        y0 = b * self.pointdist
        y1 = (b + 1) * self.pointdist

        weightx = float(x - x0) / self.pointdist
        weighty = float(y - y0) / self.pointdist

        n0 = self.dotGridGradient(a, b, x, y)
        n1 = self.dotGridGradient(a+1, b, x, y)
        ix0 = self.lerp(n0, n1, weightx)

        n0 = self.dotGridGradient(a, b+1, x, y)
        n1 = self.dotGridGradient(a+1, b+1, x, y)
        ix1 = self.lerp(n0, n1, weightx)

        return self.lerp(ix0, ix1, weighty)

    def build_mapping(self):
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                self.mapping[x][y] = self.perlin(x, y)

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
                                        max(120, 255-int(135 * val / self.scale)),                                                         int(120 * val / self.scale), 255)

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
