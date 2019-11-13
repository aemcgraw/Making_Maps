from random import randint
import math

def get_scaled_log(maximum):
    input = float(randint(1, maximum))
    initial_value = math.log(maximum / input, 10)
    scaling_factor = maximum / math.log(maximum, 10)
    temp = math.floor(initial_value * scaling_factor)
    return temp
