from PIL import Image
from random import randint

import Map

import argparse
import math

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_image", help="name of the file to output")
    parser.add_argument("x", type=int, help="horizontal size of image")
    parser.add_argument("y", type=int, help="vertical size of image")
    parser.add_argument("islands", type=int, help="number of islands in image")
    parser.add_argument("forests", type=int, help="number of forests in image")
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

    new_image = Image.new('RGBA', (args.x, args.y), (0, 0, 255, 255))
    new_im = Map.Map(new_image)
    new_im.flood()

    i = 0
    while i < args.islands:
        new_im.draw_island(get_scaled_log(100000))
        i += 1

    i = 0
    while i < args.forests:
        new_im.draw_forest(get_scaled_log(1000))
        i += 1

    new_im.save(args.output_image)
