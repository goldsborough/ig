from __future__ import print_function

import json
import os
import random

from ig import main


class Graph(object):
    def __init__(self, relation, full_path, colors, group_granularity):
        self.edges = []
        self.nodes = {}
        self.relation = relation
        self.full_path = full_path
        self.colors = colors
        self.group_granularity = group_granularity

    def add(self, node_name, neighbors):
        color = self.colors.generate()
        node = self._get_or_add_node(node_name,
                                     color=color,
                                     size=len(neighbors))
        node['size'] = len(neighbors)

        for neighbor_name in neighbors:
            color = self.colors.generate()
            neighbor = self._get_or_add_node(neighbor_name, color=color)
            self._add_edge(node, neighbor)

    def to_json(self):
        nodes = list(self.nodes.values())
        return json.dumps(dict(nodes=nodes, edges=self.edges), indent=4)

    def write(self):
        path = os.path.join(main.WWW_PATH, 'graph.json')
        with open(path, 'w') as graph_file:
            graph_file.write(self.to_json())

    @property
    def is_empty(self):
        return len(self.nodes) == 0

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

        # Take up to the last two directory names as the group
        directories = os.path.dirname(node_name).split(os.sep)
        begin = len(directories) - self.group_granularity
        node['group'] = os.sep.join(directories[begin:begin + 2])

        node['x'] = random.random() * 0.01
        node['y'] = random.random() * 0.01

        self.nodes[node_name] = node

        return node

    def _add_edge(self, source, target, **settings):
        edge = settings
        edge['id'] = len(self.edges)
        edge['size'] = 10
        edge['type'] = 'curvedArrow'

        edge['source'] = source['id']
        edge['target'] = target['id']
        if self.relation == 'included-by':
            source, target = target, source

        self.edges.append(edge)

        return edge

    def __str__(self):
        nodes = len(self.nodes)
        edges = len(self.edges)
        return '<Graph: nodes = {0}, edges = {1}>'.format(nodes, edges)
