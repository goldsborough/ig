'use strict';

let instance = new sigma({
  renderer: {
    container: 'graph-container',
    type: 'canvas',
    skipErrors: true
  }
});

(function(instance) {
  const $ = id => document.getElementById(id);

  function createFilter(instance) {
    // Initialize the Filter API
    const filter = new sigma.plugins.filter(instance);

    setupPane(instance.graph, filter);

    function applyMinDegreeFilter(element) {
      let value = element.target.value;
      $('min-degree-val').textContent = value;

      filter
        .undo('min-degree')
        .nodesBy(node => instance.graph.degree(node.id) >= value, 'min-degree')
        .apply();
    }

    function applyGroupFilter(element) {
      let group = element.target[element.target.selectedIndex].value;
      if (group.length > 0) {
        filter
          .undo('node-group')
          .nodesBy(node => node.group === group, 'node-group')
          .apply();
      }
    }

    // for Chrome and FF
    $('min-degree').addEventListener('input', applyMinDegreeFilter);
    // for IE10+, that sucks
    $('min-degree').addEventListener('change', applyMinDegreeFilter);
    $('node-group').addEventListener('change', applyGroupFilter);
  }

  function setupPane(graph, filter) {
    let maximumDegree = 0, categories = {};

    // Collect the maximum degree and categories.
    graph.nodes().forEach(node => {
      maximumDegree = Math.max(maximumDegree, graph.degree(node.id));
      categories[node.group] = true;
    })

    // Set the slider values.
    $('min-degree').max = maximumDegree;
    $('max-degree-value').textContent = maximumDegree;

    // Set up the node group combo box.
    const nodeGroup = $('node-group');
    Object.keys(categories).forEach(function(group) {
      if (group.length === 0) return;
      let option = document.createElement('option');
      option.text = group;
      nodeGroup.add(option);
    });
  }

  sigma.parsers.json('/tmp/graph.json', instance, () => {
    instance.refresh();
    instance.startForceAtlas2({
      worker: true,
      barnesHutOptimize: true,
      adjustSizes: true,
      slowDown: 50,
      strongGravityMode: true
    });
    setTimeout(() => instance.killForceAtlas2(), 8000);
    createFilter(instance);
  });

  sigma.plugins.dragNodes(instance, instance.renderers[0]);
})(instance);
