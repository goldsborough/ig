''' Defines the graph structure that stores the include relationships. '''

from __future__ import print_function

import json
import os
import random

from ig import paths


class Graph(object):
    '''
    Stores nodes (files) and edges (includes).

    Nodes are stored in a map from absolute filename to a dictionary, which
    holds all the information required by sigma.js (e.g. ID and label). Edges
    are stored as a list of (id, source, target) objects, along with some
    additional information. The representation is not very compact or optimal,
    but processing even very large projects still seems instant.
    '''
    def __init__(self, relation, full_path, colors, group_granularity):
        '''
        Constructor.

        Args:
            relation: One of {'includes', 'included-by'}
            full_path: Whether to print node labels with their full path
            colors: A `Colors` object storing information about the color scheme
            group_granularity: The granularity setting for node groups
        '''
        assert relation in ('includes', 'included-by')

        self.edges = []
        self.nodes = {}
        self.is_included_by_relation = (relation == 'included-by')
        self.use_full_path = full_path
        self.colors = colors
        self.group_granularity = group_granularity

    def add(self, node_name, neighbors):
        '''
        Adds a new node to the graph, along with its adjacent neighbors.

        Args:
            node_name: The name of the node (i.e. current file)
            neighbors: A list of names of neighbors (included files)
        '''
        node = self._get_or_add_node(node_name)

        if not self.is_included_by_relation:
            node['size'] = len(neighbors)

        for neighbor_name in neighbors:
            neighbor = self._get_or_add_node(neighbor_name)
            if self.is_included_by_relation:
                neighbor['size'] += 1
            self._add_edge(node, neighbor)

    def to_json(self):
        '''
        Turns the graph into a JSON file.

        The format is {"nodes": list of node objects, "edges": array of edge
        objects}.

        Returns:
            A JSON representation of the graph.
        '''
        nodes = list(self.nodes.values())
        return json.dumps(dict(nodes=nodes, edges=self.edges), indent=4)

    def write(self):
        '''
        Writes the graph's JSON representation to disk.

        The location is pre-determined to be in the `www` folder, for rendering.
        '''
        path = os.path.join(paths.WWW, 'graph.json')
        with open(path, 'w') as graph_file:
            graph_file.write(self.to_json())

    @property
    def is_empty(self):
        '''
        Returns:
            True if the graph has no nodes at all, else False.
        '''
        return len(self.nodes) == 0

    def _get_or_add_node(self, node_name):
        '''
        Returns a node and possibly adds it to the graph.

        Args:
            node_name: The name of the node to fetch

        Returns:
            The node entry for the given name.
        '''
        node = self.nodes.get(node_name)
        if node is None:
            node = self._add_node(node_name)
        return node

    def _add_node(self, node_name):
        '''
        Adds a node to the graph.

        Args:
            node_name: The name of the node to add

        Returns:
            The newly created node object.
        '''
        assert node_name not in self.nodes

        node = {}
        node['id'] = len(self.nodes)
        node['size'] = 1
        node['color'] = self.colors.generate()

        if self.use_full_path:
            node['label'] = node_name
        else:
            node['label'] = os.path.basename(node_name)

        # Take up to the last two directory names as the group
        directories = os.path.dirname(node_name).split(os.sep)
        begin = len(directories) - self.group_granularity
        node['group'] = os.sep.join(directories[begin:begin + 2])

        # Make the initial starting point random, but very small, so we get
        # an "explosion"/"expansion" effect.
        node['x'] = random.random() * 0.01
        node['y'] = random.random() * 0.01

        self.nodes[node_name] = node

        return node

    def _add_edge(self, source, target):
        '''
        Adds an edge to the graph.

        Args:
            source: The entry of the source node
            target: The entry of the target node

        Returns:
            The newly created edge object
        '''
        edge = {}
        edge['id'] = len(self.edges)
        edge['size'] = 10  # Make the arrows larger?
        edge['type'] = 'curvedArrow'

        # The natural direction is "includes", so swap if we want "included-by"
        if self.is_included_by_relation:
            source, target = target, source
        edge['source'] = source['id']
        edge['target'] = target['id']

        self.edges.append(edge)

        return edge

    def __repr__(self):
        '''
        Returns:
            A string representation of the graph.
        '''
        nodes = len(self.nodes)
        edges = len(self.edges)
        return '<Graph: nodes = {0}, edges = {1}>'.format(nodes, edges)
