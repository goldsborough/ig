import random


def random_color(base, variation):
    color = base + (2 * random.random() - 1) * variation
    return max(8, min(int(color), 256))


class Colors(object):
    def __init__(self, base_colors):
        self.base = list(base_colors)
        self.variation = None
        self.alpha_min = None

    def generate(self):
        rgba = [random_color(color, self.variation) for color in self.base]
        rgba.append(max(self.alpha_min, random.random()))
        return 'rgba({0})'.format(','.join(map(str, rgba)))
