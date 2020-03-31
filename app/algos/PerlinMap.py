from PIL import Image

from random import randint
from random import uniform

import math

from app.components.HeightMap import HeightMap

class PerlinMap(HeightMap):
    def __init__(self, width, height, pointdist = 10):
        super().__init__(width, height)
        self.scale = (math.sqrt(2) / 2) * pointdist

        self.wfunc = self.smoothstep
        self.pointdist = pointdist
        self.grid_points =  self._get_grid_points()
        
        self.build_mapping()
        self.fuzz()

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

        #Make left and right edges of the map identically. Makes world into a disc
        for y in range(len(rows[0])):
            rows[-1][y] = rows[0][y]

        return rows       

    def _get_grid_index(self, x, y):
        xgrid = int(x / self.pointdist)
        ygrid = int(y / self.pointdist)
        return (xgrid, ygrid)

    def lerp(self, a0, a1, x, x0):
        w = float(x - x0) / self.pointdist
        return a0 + w * ( a1 - a0 )

    def smoothstep(self, a0, a1, x, x0):
        w = float(x - x0) / self.pointdist
        step = w * w * ( 3 - ( 2 * w ) )
        return a0 + step * ( a1 - a0 )

    def dotGridGradient(self, a, b, x, y):
        ix = a * self.pointdist
        iy = b * self.pointdist

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

        n0 = self.dotGridGradient(a, b, x, y)
        n1 = self.dotGridGradient(a+1, b, x, y)
        ix0 = self.wfunc(n0, n1, x, x0)

        n0 = self.dotGridGradient(a, b+1, x, y)
        n1 = self.dotGridGradient(a+1, b+1, x, y)
        ix1 = self.wfunc(n0, n1, x, x0)

        return self.wfunc(ix0, ix1, y, y0)

    def build_mapping(self):
        for x in range(len(self.mapping)):
            for y in range(len(self.mapping[x])):
                self.mapping[x][y] = self.perlin(x, y)
