from __future__ import print_function

import argparse
import os
import sys

from ig import colors, graph, server, walk


def parse_arguments(args):
    '''
    Sets up the command line argument parser and parses arguments.

    Args:
        args: The list of argumnets passed to the command line

    Returns:
        The parsed arguments.
    '''
    parser = argparse.ArgumentParser(description='Visualize C++ include graphs')
    parser.add_argument('directories',
                        nargs='+',
                        help='The directories to look at')
    parser.add_argument('-p', '--pattern',
                        action='append',
                        default=['*.[ch]pp', '*.[ch]'],
                        dest='patterns',
                        help='The file (glob) patterns to look for')
    parser.add_argument('-i', '-I', '--prefix',
                        action='append',
                        dest='prefixes',
                        default=[os.getcwd()],
                        help='An include path for headers to recognize')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Whether to turn on verbose output')

    parser.add_argument('--port',
                        type=int,
                        default=8080,
                        help='The port to serve the visualization on')
    parser.add_argument('-o', '--open',
                        action='store_true',
                        help='Whether to open the webpage immediately')
    parser.add_argument('-j', '--json',
                        action='store_true',
                        help='Whether to print the graph JSON and not serve it')

    parser.add_argument('--relation',
                        choices=['includes', 'included-by'],
                        default='included-by',
                        help='The relation of edges in the graph')
    parser.add_argument('--group-granularity',
                        type=int,
                        default=2,
                        help='How coarse to group nodes (by folder)')
    parser.add_argument('--full-path',
                        action='store_true',
                        help='If set, shows the full path for nodes')
    parser.add_argument('--colors',
                        type=lambda p: colors.Colors(map(int, p.split(','))),
                        default='234, 82, 77',
                        help='The base RGB colors separated by commas')
    parser.add_argument('--color-variation',
                        type=int,
                        default=200,
                        help='The variation in RGB around the base colors')
    parser.add_argument('--color-alpha-min',
                        type=float,
                        default=0.7,
                        help='The minimum alpha value for colors')

    args = parser.parse_args(args)

    # Necessary for standard includes
    args.prefixes.append('')

    if not (0 <= args.color_alpha_min <= 1):
        raise RuntimeError('--color-alpha-min must be in interval [0, 1]')

    args.colors.variation = args.color_variation
    args.colors.alpha_min = args.color_alpha_min

    return args


def main():
    args = parse_arguments(sys.argv[1:])
    include_graph = graph.Graph(args.relation,
                                args.full_path,
                                args.colors,
                                args.group_granularity)
    walk.walk(include_graph, args)

    if include_graph.is_empty:
        if args.verbose:
            print('Could not find a single file', file=sys.stderr)
        return -1

    if args.json:
        print(include_graph.to_json())
    else:
        include_graph.write()
        server.serve(args.open, args.port)

if __name__ == '__main__':
    main()
