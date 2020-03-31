from PIL import Image
from random import randint

from app.algos.PerlinMap import PerlinMap
from app.algos.DiamondSquareMap import DiamondSquareMap
from app.components.ColorMap import ColorMap
#from algos.DiamondSquareMap_wrap import DiamondSquareMap_wrap
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

def get_scaled_log(maximum):
    input = float(randint(1, maximum))
    print(input)
    initial_value = math.log(maximum / input, 10)
    scaling_factor = maximum / math.log(maximum, 10)
    temp = math.floor(initial_value * scaling_factor)
    print(temp)
    return temp

if __name__ == "__main__":
    args = parse()

    image1 = Image.new('RGBA', (args.x, args.y), (0, 255, 0, 255))
    #image2 = Image.new('RGBA', (args.x, args.y), (0, 0, 0, 0))
    
    ht1 = DiamondSquareMap(image1,damping=0.8,chaos=1.0,delay=args.delay,verbose=args.verbose)
    #ht2 = DiamondSquareMap(image2,damping=0.8,chaos=1.0,delay=args.delay,verbose=args.verbose)
    cm1 = ColorMap(image1, ht1)
    #cm2 = ColorMap(image2, ht2)

    #adjust = ht2.get_low_median()
    #print(str(adjust))
    #ht2.adjust_global(adjust)

    cm1.std()
    #cm2.forest_nothing()

    #image1.alpha_composite(image2)
    image1.save(args.output_image, format='PNG')
