import random

def pick_from_list(probability_choices):
    pick = random.random()
    for prob, choice in probability_choices:
        if prob > pick:
            return choice

    return probability_choices[-1][1]

def generate_shade_of_light_grey():
    return __generate_shade_of_grey(random.randint(192, 255))

def generate_shade_of_dark_grey():
    return __generate_shade_of_grey(random.randint(4, 96))

def __generate_shade_of_grey(base):
    value_range = 4
    vary_by = value_range / 2
    red = max(0, min(255, base + random.randint(0, value_range) - vary_by))
    blue = max(0, min(255, base + random.randint(0, value_range) - vary_by))
    green = max(0, min(255, base + random.randint(0, value_range) - vary_by))

    color = "#%02x%02x%02x" % (int(red), int(green), int(blue))
    return color

def generate_background_color():
    value_range = 200
    vary_by = value_range / 2
    red = max(0, random.randint(64, value_range))
    blue = max(0, random.randint(64, value_range))
    green = max(0, random.randint(64, value_range))

    color = "#%02x%02x%02x" % (int(red), int(green), int(blue))
    return color

