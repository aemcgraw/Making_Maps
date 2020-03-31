from PIL import Image
from random import randint

from app.algos.PerlinMap import PerlinMap
from app.algos.DiamondSquareMap import DiamondSquareMap
from app.components.ColorMap import ColorMap
from app.components.RegionMap import RegionMap
from app.components.RegionID import RegionID_forest
from app.algos.StripeyMap import StripeyMap

import argparse
import math

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_image", help="name of the file to output")
    parser.add_argument("x", type=int, help="horizontal size of image")
    parser.add_argument("y", type=int, help="vertical size of image")
    parser.add_argument("--delay", type=int, default=0, help="delay")
    parser.add_argument("--verbose", action='store_true', help="verbose")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse()

    image1 = Image.new('RGBA', (args.x, args.y), (0, 0, 0, 255))
    
    ht1 = DiamondSquareMap(args.x,args.y,damping=0.8,chaos=1.0,delay=args.delay,verbose=args.verbose)
    rid = RegionID_forest()
    rm1 = RegionMap(image1, ht1, rid)

    rm1.outline_regions()
    image1.save('x1.png', format='PNG')

    rm1.color_regions()
    image1.save('x2.png', format='PNG')
