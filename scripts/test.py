from PIL import Image
from random import randint

from app.algos.SimpleMap import SimpleMap
from app.algos.PerlinMap import PerlinMap
from app.algos.DiamondSquareMap import DiamondSquareMap
from app.algos.DiamondSquareMap_wrap import DiamondSquareMap_wrap
from app.components.ColorMap import ColorMap
from app.algos.StripeyMap import StripeyMap

import argparse
import math

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, help="horizontal size of image")
    parser.add_argument("y", type=int, help="vertical size of image")
    parser.add_argument("--verbose", action='store_true', help="verbose")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse()

    map1 = SimpleMap(args.x, args.y)
    map1.draw_island(100)
    map1.draw_forest(50)
    map1.image.save('testsimplemap.png', format='PNG')

    map2 = DiamondSquareMap(args.x, args.y,damping=0.8,chaos=1.0)
    cm2 = ColorMap(map2)
    cm2.std()
    map2.image.save('testdsbmap.png', format='PNG')

    map3 = StripeyMap(args.x, args.y)
    cm3 = ColorMap(map3)
    cm3.std()
    map3.image.save('teststripeymap.png', format='PNG')

    map4 = PerlinMap(args.x, args.y)
    cm4 = ColorMap(map4)
    cm4.std()
    map4.image.save('testperlinmap.png', format='PNG')

    map5 = DiamondSquareMap_wrap(args.x, args.y)
    cm5 = ColorMap(map5)
    cm5.std()
    map5.image.save('testdbs_wrapmap.png', format='PNG')
