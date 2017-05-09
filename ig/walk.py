from __future__ import print_function

import fnmatch
import os
import re
import sys


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


def glob(directory, pattern):
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def walk(graph, args):
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

    print('Result: {0}'.format(graph), file=sys.stderr)
