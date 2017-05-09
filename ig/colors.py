import random


def random_color(base, variation):
    '''
    Returns a random, bounded color value.

    Args:
        base: Some base color component (between 0 and 255)
        variation: The degree of variation (around the color)

    Returns:
        A random color.
    '''
    color = base + (2 * random.random() - 1) * variation
    return max(8, min(int(color), 256))


class Colors(object):
    '''
    Aggregates information about the color scheme of the visualization.
    '''

    def __init__(self, base_colors):
        '''
        Constructor.

        Args:
            base_colors: The base colors around which to vary
        '''
        self.base = list(base_colors)
        self.variation = None
        self.alpha_min = None

    def generate(self):
        '''
        Generates a color.

        Returns:
            A new RGBA color value.
        '''
        rgba = [random_color(color, self.variation) for color in self.base]
        rgba.append(max(self.alpha_min, random.random()))
        return 'rgba({0})'.format(','.join(map(str, rgba)))
