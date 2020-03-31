#DiamondSquareMap with wraparound, currently appears to be broken. Can't recommend

from PIL import Image

from random import randint
from random import uniform

import math

from app.components.HeightMap import HeightMap

class DiamondSquareMap_wrap(HeightMap):
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
        rows[0] = rows[-1]
        return rows

    def test_point(self, x, bx, maxedge):
        if x - bx < 0 or x + bx >= maxedge:
            return False
        return True

    def random_grid(self, gridsize, boxmap):
        for x in range(0, totalsize, gridsize):
            for y in range(0, totalsize, gridsize):
                boxmap[x][y] = uniform(-self.chaos, self.chaos)

    def diamond(self, bx, totalsize, boxmap):
        chaos = self.chaos

        newbx = int(bx / 2)
        for x in range(0, totalsize - bx, bx):
            for y in range(0, totalsize - bx, bx):
                #Diamond
                centerx = x + newbx
                centery = y + newbx
                bx1 = boxmap[x][y]
                bx2 = boxmap[x + bx][y]
                bx3 = boxmap[x][y + bx]
                bx4 = boxmap[x + bx][y + bx]
                boxmap[centerx][centery] = ((bx1 + bx2 + bx3 + bx4) / 4) + uniform(-chaos, chaos)

    def box_restricted(self, bx, totalsize, boxmap):
        chaos = self.chaos

        newbx = int(bx / 2)
        for x in range(0, totalsize - bx, bx):
            for y in range(0, totalsize - bx, bx):
                bx1 = boxmap[x][y]
                bx2 = boxmap[x + bx][y]
                bx3 = boxmap[x][y + bx]
                bx4 = boxmap[x + bx][y + bx]

                centerx = x + newbx
                centery = y + newbx
                bx5 = boxmap[centerx][centery]

                boxmap[centerx][y] = ((bx5 + bx1 + bx2) / 3 + uniform(-chaos, chaos))
                boxmap[centerx][y + bx] = ((bx5 + bx3 + bx4) / 3 + uniform(-chaos, chaos))
                boxmap[x][centery] = ((bx5 + bx1 + bx3) / 3 + uniform(-chaos, chaos))
                boxmap[x + bx][centery] = ((bx5 + bx2 + bx4) / 3 + uniform(-chaos, chaos))

    def box(self, bx, totalsize, boxmap):
        chaos = self.chaos
        esize = totalsize - 1

        newbx = int(bx / 2)
        for x in range(0, totalsize - bx, bx):
            for y in range(0, totalsize - bx, bx):
                bx1 = boxmap[x][y]
                bx2 = boxmap[x + bx][y]
                bx3 = boxmap[x][y + bx]
                bx4 = boxmap[x + bx][y + bx]

                centerx = x + newbx
                centery = y + newbx
                bx5 = boxmap[centerx][centery]

                #TODO : Take averages properly

                if self.test_point(y, newbx, totalsize):
                    (bx5 + bx1 + bx2 + boxmap[centerx][y - newbx]) / 4
                else:
                    (bx5 + bx1 + bx2) / 3

                boxmap[centerx][y] = (((bx5 + bx1 + bx2 + boxmap[centerx][y - newbx]) / 4) 
                                        if self.test_point(y, newbx, totalsize) 
                                        else ((bx5 + bx1 + bx2) / 3) +
                                        uniform(-chaos, chaos))
                boxmap[centerx][y + bx] = (((bx5 + bx3 + bx4 + boxmap[centerx][y + bx + newbx]) / 4) 
                                            if self.test_point(y + bx, newbx, totalsize)
                                            else ((bx5 + bx3 + bx4) / 3) +
                                            uniform(-chaos, chaos))
                boxmap[x][centery] = (bx5 + bx1 + bx3 + boxmap[(x - newbx) % esize][centery]) / 4
                boxmap[x + bx][centery] = (bx5 + bx2 + bx4 + boxmap[(x + bx + newbx) % esize][centery]) / 4

                #boxmap[x][centery] = (((bx5 + bx1 + bx3 + boxmap[x - newbx][centery]) / 4) 
                #                        if self.test_point(x, newbx, totalsize) 
                #                        else ((bx5 + bx1 + bx3) / 3) +
                #                        uniform(-chaos, chaos))
                #boxmap[x + bx][centery] = (((bx5 + bx2 + bx4 + boxmap[x + bx + newbx][centery]) / 4)
                #                            if self.test_point(x + bx, newbx, totalsize) 
                #                            else ((bx5 + bx2 + bx4) / 3) +
                #                            uniform(-chaos, chaos))


    def setup(self, boxmap, x, y):
        boxmap[x][y] = uniform(-self.chaos, self.chaos)
        if self.verbose:
            print(str(boxmap[x][y]))

    def build_mapping(self):
        bx = 1
        while (bx + 1) < max(self.image.width, self.image.height):
            bx = bx * 2
        totalsize = bx + 1
        boxmap = self._get_box(bx + 1)

        self.setup(boxmap, 0, 0)
        self.setup(boxmap, bx, 0)
        self.setup(boxmap, 0, bx)
        self.setup(boxmap, bx, bx)

        while ( bx / 2 ) >= 1:
            if self.delay > 0:
                print(str(self.delay))
                self.delay -= 1
                if self.delay == 0 and self.verbose:
                    for x in range(0, totalsize, bx):
                        print(str([x for x in boxmap[x] if x != 0]))
            else:
                self.chaos = self.chaos * self.damping

            newbx = int(bx / 2)

            self.diamond(bx, totalsize, boxmap)
            self.box(bx, totalsize, boxmap)

            bx = newbx

        for x in range(self.image.width):
            for y in range(self.image.height):
                self.mapping[x][y] = boxmap[x][y]
