import argparse
import collections
import glob
import json
import os
import random
import re
import sys


class Colors(object):
    def __init__(self, base_colors):
        self.base = list(base_colors)
        self.variation = None
        self.alpha_min = None

    @staticmethod
    def to_string(rgba):
        return 'rgba({0})'.format(','.join(map(str, rgba)))


def random_color(base, variation):
    color = base + (2 * random.random() - 1) * variation
    return max(8, min(int(color), 256))


def generate_color(colors):
    rgba = [random_color(color, colors.variation) for color in colors.base]
    rgba.append(max(colors.alpha_min, random.random()))
    # colors = [random.randrange(32, 256) for _ in 'rgb']
    return Colors.to_string(rgba)


class Graph(object):
    def __init__(self, directed, full_path, colors):
        self.edges = []
        self.nodes = {}
        self.directed = directed
        self.full_path = full_path
        self.colors = colors

    def add(self, node_name, neighbors):
        color = generate_color(self.colors)

        node = self._get_or_add_node(node_name,
                                     color=color,
                                     size=len(neighbors))
        node['size'] = len(neighbors)

        for neighbor_name in neighbors:
            color = generate_color(self.colors)
            neighbor = self._get_or_add_node(neighbor_name, color=color)
            self._add_edge(node, neighbor)

    def to_json(self):
        self.resize()
        nodes = list(self.nodes.values())
        return json.dumps(dict(nodes=nodes, edges=self.edges), indent=4)

    def resize(self):
        pass

    def _get_or_add_node(self, node_name, **settings):
        node = self.nodes.get(node_name)
        if node is None:
            node = self._add_node(node_name, **settings)
        return node

    def _add_node(self, node_name, **settings):
        assert node_name not in self.nodes

        node = settings
        node['id'] = len(self.nodes)
        node['size'] = settings.get('size', 1)

        if self.full_path:
            node['label'] = node_name
        else:
            node['label'] = os.path.basename(node_name)

        directory = os.path.dirname(node_name)
        node['group'] = directory

        node['x'] = random.random() * 0.01
        node['y'] = random.random() * 0.01

        self.nodes[node_name] = node

        return node

    def _add_edge(self, source, target, **settings):
        edge = settings
        edge['id'] = len(self.edges)
        edge['size'] = random.random()

        edge['source'] = source['id']
        edge['target'] = target['id']
        if self.directed == 'included-by':
            source, target = target, source

        if self.directed:
            edge['type'] = 'curvedArrow'

        self.edges.append(edge)

        return edge

    def __str__(self):
        nodes = len(self.nodes)
        edges = len(self.edges)
        return '<Graph: nodes = {0}, edges = {1}>'.format(nodes, edges)


def try_prefixes(path, prefixes):
    for prefix in prefixes:
        full_path = os.path.realpath(os.path.join(prefix, path))
        if os.path.exists(full_path):
            return full_path

    return path


def get_includes(filename, prefixes):
    pattern = re.compile(r'^#include ["<](.*)[">]$')
    includes = set()
    with open(filename) as source:
        for line in source:
            match = pattern.match(line)
            if match is not None:
                full_path = try_prefixes(match.group(1), prefixes)
                includes.add(full_path)

    return includes


def walk(args):
    graph = Graph(args.directed, args.full_path, args.colors)
    for directory in args.directories:
        for pattern in args.patterns:
            path = os.path.realpath(directory)
            full_pattern = '{0}/**/{1}'.format(path, pattern)
            print('Globbing for {0}'.format(full_pattern), file=sys.stderr)
            for filename in glob.iglob(full_pattern, recursive=True):
                includes = get_includes(filename, [path] + args.prefixes)
                graph.add(filename, includes)

    return graph


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('directories',
                        nargs='+',
                        help='The directories to look at')
    parser.add_argument('--patterns',
                        nargs='+',
                        default=['*.[ch]pp', '*.[ch]'],
                        help='The file (glob) patterns to look for')
    parser.add_argument('--directed',
                        action='store_true',
                        help="If set, draws directed edges.")
    parser.add_argument('--relation',
                        choices=['includes', 'included-by'],
                        help="If '--directed' is set, specifies the relation "
                             "of edges ")
    parser.add_argument('--full-path',
                        action='store_true',
                        help='If set, shows the full path for nodes')
    parser.add_argument('--prefix',
                        action='append',
                        dest='prefixes',
                        default=[os.getcwd()],
                        help='An include path for headers to recognize')
    parser.add_argument('--colors',
                        type=lambda p: Colors(map(int, p.split(','))),
                        default='234, 82, 77',
                        help='The base rgb colors separated by commas')
    parser.add_argument('--color-variation',
                        type=int,
                        default=200,
                        help='The variation in RGB around the base colors')
    parser.add_argument('--color-alpha-min',
                        type=float,
                        default=0.5,
                        help='The minimum alpha value for colors')

    args = parser.parse_args(args)

    if args.directed and args.relation:
        args.directed = args.relation

    if not (0 <= args.color_alpha_min <= 1):
        raise RuntimeError('--color-alpha-min must be in interval [0, 1]')

    args.colors.variation = args.color_variation
    args.colors.alpha_min = args.color_alpha_min

    return args


def main():
    args = parse_arguments(sys.argv[1:])
    graph = walk(args)
    print('Result: {0}'.format(graph), file=sys.stderr)

    print(graph.to_json())


if __name__ == '__main__':
    main()
