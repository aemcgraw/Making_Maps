from PIL import Image
from random import randint

from PerlinMap import PerlinMap
from DiamondSquareMap import DiamondSquareMap

import argparse
import math

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_image", help="name of the file to output")
    parser.add_argument("x", type=int, help="horizontal size of image")
    parser.add_argument("y", type=int, help="vertical size of image")
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

    new_image = Image.new('RGBA', (args.x, args.y), (0, 255, 0, 255))
    ht = DiamondSquareMap(new_image)
    #ht = PerlinMap(new_image, pointdist=10)
    #ht.add(ht2)
    ht.heightmap_to_image()

    ht.image.save(args.output_image, format='PNG')
