'''Entry point and command line parsing for ig.'''

from __future__ import print_function

import argparse
import logging
import os
import sys

from ig import colors, graph, serve, walk


def setup_logging():
    '''Sets up the root logger.'''
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    log = logging.getLogger(__package__)
    log.addHandler(handler)
    log.setLevel(logging.INFO)

    return log


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
    parser.add_argument('--pattern',
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

    parser.add_argument('-p', '--port',
                        type=int,
                        default=8080,
                        help='The port to serve the visualization on')
    parser.add_argument('-o', '--open',
                        action='store_true',
                        help='Whether to open the webpage immediately')
    parser.add_argument('-j', '--json',
                        action='store_true',
                        help='Whether to print the graph JSON and not serve it')
    parser.add_argument('-d', '--dir',
                        dest='directory',
                        help='The directory to store the served files in. If'
                             'not supplied, a temporary directory is created.')

    parser.add_argument('--relation',
                        choices=['includes', 'included-by'],
                        default='included-by',
                        help='The relation of edges in the graph')
    parser.add_argument('--min-degree',
                        type=float,
                        default=0.1,
                        help='The initial minimum degree nodes should have to '
                             'be displayed')
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


def make_json(args, graph_json):
    if args.json:
        print(graph_json)
        sys.exit(0)

    # Additional settings to configure the visualization
    settings = dict(initialDegree=args.min_degree)

    return dict(settings=settings, graph=graph_json)


def main():
    log = setup_logging()

    args = parse_arguments(sys.argv[1:])
    if args.verbose:
        log.setLevel(logging.DEBUG)
    log.debug('Received arguments: %s', args)

    include_graph = graph.Graph(args.relation,
                                args.full_path,
                                args.colors,
                                args.group_granularity)
    walk.walk(include_graph, args)

    if include_graph.is_empty:
        log.debug('Could not find a single node, exiting')
        sys.exit(-1)

    json = make_json(args, include_graph.to_json())

    with serve.Server(args.directory) as server:
        server.write(json)
        server.run(args.open, args.port)

    log.info('Shutting down')

if __name__ == '__main__':
    main()
