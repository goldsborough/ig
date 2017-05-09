from __future__ import print_function

import fnmatch
import os
import re
import sys


INCLUDE_PATTERN = re.compile(r'^#include ["<](.*)[">]$')


def try_prefixes(path, prefixes):
    '''
    Tries to prepend a list of prefixes to a path to see if any exists.

    This is necessary to ensure that we have unique file paths, even if the same
    file is specified differently (sometimes relative to one directory, then to
    another etc.).

    Args:
        path: The path to append to the prefixes
        perfixes: The prefixes to prepend to the path

    Returns:
        The best possible path.
    '''
    for prefix in prefixes:
        full_path = os.path.realpath(os.path.join(prefix, path))
        if os.path.exists(full_path):
            return full_path

    return path


def get_includes(filename, prefixes):
    '''
    Parses out the includes from a file.

    Args:
        filename: The name of the file to get includes for
        prefixes: The prefixes under which to search for includes

    Returns:
        A list of includes for the file.
    '''
    includes = set()
    with open(filename) as source:
        for line in source:
            match = INCLUDE_PATTERN.match(line)
            if match is not None:
                full_path = try_prefixes(match.group(1), prefixes)
                includes.add(full_path)

    return includes


def glob(directory, pattern):
    '''
    Globs for files patterns under a directory.

    There is a `glob` module, but its recursive variant only works in Python3.
    This is a short DIY version of recursive globbing.

    Args:
        directory: The root directory
        pattern: The pattern to glob for

    Yields:
        Any matching files (with absolute paths).
    '''
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def walk(graph, args):
    '''
    Walks the file tree, populating the graph.

    Args:
        graph: The empty graph to populate
        args: The arguments passed to the command line

    Returns:
        The (possibly) populated graph.
    '''
    for directory in args.directories:
        # Swap pattern <-> filename loops if too inefficient
        for pattern in args.patterns:
            path = os.path.realpath(directory)
            for filename in glob(path, pattern):
                if os.path.isdir(filename):
                    if args.verbose:
                        print('{0} is a directory, skipping'.format(filename),
                              file=sys.stderr)
                    continue
                includes = get_includes(filename, [path] + args.prefixes)
                graph.add(filename, includes)

    print('Result: {0}'.format(repr(graph)), file=sys.stderr)
