from PIL import Image

from random import randint
from random import uniform

import math

from HeightMap import HeightMap

class DiamondSquareMap(HeightMap):
    def __init__(self, image, chaos=1.0, damping=0.75, verbose=False):
        super().__init__(image)
        self.scale = 1
        self.damping = damping
        self.chaos = chaos

        self.mapping = self._get_setup() 
        self.build_mapping()
        #self.fuzz()

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

    def build_mapping(self):
        maxedge = max(self.image.width, self.image.height)
        chaos = self.chaos
        bx = 4
        while (bx + 1) < maxedge:
            bx = bx * 2

        boxmap = self._get_box(bx + 1)

        totalsize = bx + 1
        ix = 0
        iy = 0

        #bx1 = boxmap[ix][ix] = uniform(-chaos, chaos)
        #bx2 = boxmap[bx][ix] = uniform(-chaos, chaos)
        #bx3 = boxmap[ix][bx] = uniform(-chaos, chaos)
        #bx4 = boxmap[bx][bx] = uniform(-chaos, chaos)

        bx1 = boxmap[ix][ix] = uniform(-1.0, 1.0)
        bx2 = boxmap[bx][ix] = uniform(-1.0, 1.0)
        bx3 = boxmap[ix][bx] = uniform(-1.0, 1.0)
        bx4 = boxmap[bx][bx] = uniform(-1.0, 1.0)

        #while ( bx / 2 ) >= 256:
        #    print("Random")
        #    newbx = int(bx / 2)
        #    for x in range(0, totalsize - bx, bx):
        #        for y in range(0, totalsize - bx, bx):
        #            #Diamond
        #            centerx = x + newbx
        #            centery = y + newbx
        #            bx5 = boxmap[centerx][centery] = uniform(-chaos, chaos)

        #    for x in range(0, totalsize - bx, bx):
        #        for y in range(0, totalsize - bx, bx):
        #            centerx = x + newbx
        #            centery = y + newbx
        #            #Box
        #            boxmap[centerx][y] = uniform(-chaos, chaos)
        #            boxmap[centerx][y + bx] = uniform(-chaos, chaos)
        #            boxmap[x][centery] = uniform(-chaos, chaos)
        #            boxmap[x + bx][centery] = uniform(-chaos, chaos)
        #    bx = newbx

        #for x in range(0, totalsize, bx):
        #    print(str([x for x in boxmap[x] if x != 0]))
  
        #chaos = chaos * damping * damping
        while ( bx / 2 ) >= 1:
            chaos = chaos * self.damping

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
                    bx5 = boxmap[centerx][centery] = ((bx1 + bx2 + bx3 + bx4) / 4) + uniform(-chaos, chaos)

            for x in range(0, totalsize - bx, bx):
                for y in range(0, totalsize - bx, bx):
                    bx1 = boxmap[x][y]
                    bx2 = boxmap[x + bx][y]
                    bx3 = boxmap[x][y + bx]
                    bx4 = boxmap[x + bx][y + bx]

                    centerx = x + newbx
                    centery = y + newbx
                    bx5 = boxmap[centerx][centery]
                    #Box
                    #TODO : Take averages properly
                    #boxmap[centerx][y] = ((bx5 + bx1 + bx2) / 3 + uniform(-chaos, chaos))
                    #boxmap[centerx][y + bx] = ((bx5 + bx3 + bx4) / 3 + uniform(-chaos, chaos))
                    #boxmap[x][centery] = ((bx5 + bx1 + bx3) / 3 + uniform(-chaos, chaos))
                    #boxmap[x + bx][centery] = ((bx5 + bx2 + bx4) / 3 + uniform(-chaos, chaos))

                    boxmap[centerx][y] = ((bx5 + bx1 + bx2 + 
                        (boxmap[centerx][y - newbx] if self.test_point(y, newbx, totalsize) else 0)) / 4 +
                        uniform(-chaos, chaos))
                    boxmap[centerx][y + bx] = ((bx5 + bx3 + bx4 + 
                        (boxmap[centerx][y + bx + newbx] if self.test_point(y + bx, newbx, totalsize) else 0)) / 4 +
                        uniform(-chaos, chaos))
                    boxmap[x][centery] = ((bx5 + bx1 + bx3 + 
                        (boxmap[x - newbx][centery] if self.test_point(y + bx, newbx, totalsize) else 0)) / 4 +
                        uniform(-chaos, chaos))
                    boxmap[x + bx][centery] = ((bx5 + bx2 + bx4 +
                        (boxmap[x + bx + newbx][centery] if self.test_point(x + bx, newbx, totalsize) else 0)) / 4 +
                        uniform(-chaos, chaos))

            bx = newbx

        for x in range(self.image.width):
            for y in range(self.image.height):
                self.mapping[x][y] = boxmap[x][y]
