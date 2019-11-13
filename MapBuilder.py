from PIL import Image

import Map
import util

def generate_random_map():
    new_image = Image.new('RGBA', (400, 400), (0, 0, 255, 255))
    new_im = Map.Map(new_image)
    new_im.flood()

    i = 0
    while i < 10:
        new_im.draw_island(util.get_scaled_log(10000))
        i += 1

    i = 0
    while i < 5:
        new_im.draw_forest(util.get_scaled_log(4000))
        i += 1

    #TODO : Change hardcoded path
    new_im.save("/Users/mcgraw/Making_Maps/static/test.bmp")

    return 'test.bmp'
