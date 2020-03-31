from PIL import Image

from random import randint
from random import uniform

import math

from app.components.HeightMap import HeightMap

class StripeyMap(HeightMap):
    def __init__(self, width, height, chaos=1.0, damping=0.75, delay=0, verbose=False):
        super().__init__(width, height)
        self.scale = 1
        self.damping = damping
        self.chaos = chaos
        self.delay = delay
        self.verbose = verbose

        self.mapping = self._get_setup() 
        self.build_mapping()

    def _get_setup(self):
        rows = []
        column = [0] * self.image.height
        for x in range(self.image.width):
            rows.append(column[:])
        return rows

    def _get_box(self, size):
        rows = []
        column = [0] * size
        for x in range(size):
            rows.append(column[:])
        return rows

    def test_point(self, x, bx, maxedge):
        if x - bx < 0 or x + bx >= maxedge:
            return False
        return True

    def random_grid(self, gridsize, boxmap):
        for x in range(0, totalsize, gridsize):
            for y in range(0, totalsize, gridsize):
                boxmap[x][y] = uniform(-self.chaos, self.chaos)

    def setup(self, boxmap, x, y):
        boxmap[x][y] = uniform(-self.chaos, self.chaos)
        if self.verbose:
            print("Setup : " + str(boxmap[x][y]))

    #a0 + w * (a1 - a0)
    def lerp(self, boxmap):
        size = len(boxmap) - 1
        for y in range(0, len(boxmap[0])):
            for x in range(1, len(boxmap) - 1):
                boxmap[x][y] = boxmap[0][y] + (x / size)  * (boxmap[-1][y] - boxmap[0][y])

    def stripe(self, boxmap, index):
        self.setup(boxmap, index, 0)
        self.setup(boxmap, index, -1)

        column = boxmap[index]
        totalsize = len(column)
        size = int(len(column) - 1)
        chaos = self.chaos
        while size >= 1:
            newsize = int(size / 2)
            for y in range(0, totalsize - size, size):
                boxmap[index][y + newsize] = ((boxmap[index][y] + boxmap[index][y + size]) / 2) + uniform(-chaos, chaos)
                chaos = chaos * self.damping

            size = newsize            

    def build_mapping(self):
        bx = 1
        while (bx + 1) < max(self.image.width, self.image.height):
            bx = bx * 2
        totalsize = bx + 1
        boxmap = self._get_box(bx + 1)

        self.stripe(boxmap, 0)
        self.stripe(boxmap, -1)

        self.lerp(boxmap)

        for x in range(self.image.width):
            for y in range(self.image.height):
                self.mapping[x][y] = boxmap[x][y]
