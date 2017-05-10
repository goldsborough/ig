'use strict';

const $ = id => document.getElementById(id);

function createFilter(instance, settings) {
  // Initialize the Filter API
  const filter = new sigma.plugins.filter(instance);

  const maximumDegree = visualizePane(instance.graph, filter);

  function applyMinDegreeFilter(value) {
    if (typeof value === 'object') {
      value = value.target.value;
    }

    $('min-degree').value = value;
    $('min-degree-val').textContent = value;

    filter
      .undo('min-degree')
      .nodesBy(node => instance.graph.degree(node.id) >= value, 'min-degree')
      .apply();
  }

  function applyGroupFilter(element) {
    let group = element.target[element.target.selectedIndex].value;
    filter
      .undo('node-group')
      .nodesBy(node => !group || node.group === group, 'node-group')
      .apply();
  }

  // for Chrome and FF
  $('min-degree').addEventListener('input', applyMinDegreeFilter);
  // for IE10+, that sucks
  $('min-degree').addEventListener('change', applyMinDegreeFilter);
  $('node-group').addEventListener('change', applyGroupFilter);

  let degree = settings.initialDegree;
  if (degree < 1) {
    // Assume it's a fraction.
    degree = Math.ceil(maximumDegree * degree);
  }
  applyMinDegreeFilter(Math.min(maximumDegree, degree));
}

function visualizePane(graph, filter) {
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

  return maximumDegree;
}

function visualize(json) {
  console.log(json);

  const instance = new sigma({
    graph: json.graph,
    renderer: {
      container: 'graph-container',
      type: 'canvas',
      skipErrors: true,
      labelThreshold: 0,
      labelSize: 'proportional'
    }
  });

  instance.startForceAtlas2({
    worker: true,
    barnesHutOptimize: true,
    adjustSizes: true,
    slowDown: 20,
    strongGravityMode: true
  });

  createFilter(instance, json.settings);

  const drag = sigma.plugins.dragNodes(instance, instance.renderers[0]);
  drag.bind('startdrag', event => {
    if (instance.isForceAtlas2Running()) {
      instance.killForceAtlas2()
    }
  });
}

const xhr = new XMLHttpRequest();
xhr.open('GET', 'graph.json');
xhr.onreadystatechange = () => {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    visualize(JSON.parse(xhr.responseText));
  }
}

xhr.send();
