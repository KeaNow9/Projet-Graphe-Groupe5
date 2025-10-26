const width = window.innerWidth;
const height = document.getElementById('graph').offsetHeight;

// SVG + container (pour le zoom/pan)
const svg = d3.select('#graph').append('svg')
  .attr('width', width)
  .attr('height', height);


// Ajoute une définition de flèche (pour les graphes orientés)
const defs = svg.append('defs');
defs.append('marker')
  .attr('id', 'arrow')
  .attr('viewBox', '0 -5 10 10')
  .attr('refX', 22)
  .attr('refY', 0)
  .attr('markerWidth', 6)
  .attr('markerHeight', 6)
  .attr('orient', 'auto')
  .append('path')
  .attr('d', 'M0,-5L10,0L0,5')
  .attr('fill', '#999');

const container = svg.append('g').attr('class', 'container');

// Groupes (créés UNE FOIS, dans le container)
const linkGroup  = container.append('g').attr('class', 'links');
const nodeGroup  = container.append('g').attr('class', 'nodes');
const labelGroup = container.append('g').attr('class', 'labels');

// Zoom / pan
const zoom = d3.zoom()
  .scaleExtent([0.3, 3])
  .on('zoom', (event) => container.attr('transform', event.transform));
svg.call(zoom);

let simulation;            // simulation au scope global (réassignée à chaque rendu)
let graphData = {nodes:[], links:[]};

function fit(){
  const bounds = container.node().getBBox();
  const fullWidth = width, fullHeight = height;
  if (!bounds.width || !bounds.height) return;
  const midX = bounds.x + bounds.width / 2;
  const midY = bounds.y + bounds.height / 2;
  const scale = 0.9 / Math.max(bounds.width / fullWidth, bounds.height / fullHeight);
  const translate = [fullWidth/2 - scale*midX, fullHeight/2 - scale*midY];
  svg.transition().duration(500)
     .call(zoom.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
}

function renderGraph(data){
  graphData = data;

  const distScale = d3.scaleSqrt()
    .domain(d3.extent(data.links, d => d.weight || 1))
    .range([40, 120]); // compresse les grands poids

  // (ré)crée la simulation
  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links)
      .id(d => d.id)
      .distance(d => distScale(d.weight || 1)))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width/2, height/2))
    .force('collision', d3.forceCollide(28));

  // L I N K S
  const links = linkGroup.selectAll('line')
    .data(data.links, d => (d.source.id || d.source) + '-' + (d.target.id || d.target));

  links.exit().remove();

  const linksEnter = links.enter()
  .append('line')
  .attr('class','link')
  if (data.directed) {
  linksEnter.attr('marker-end', 'url(#arrow)');
  }

  linksEnter.append('title');
  linksEnter.merge(links).select('title').text(d => `w=${d.weight}`);

  // --- L A B E L S  (poids des arêtes) ---
const labels = labelGroup.selectAll('text')
  .data(data.links, d => (d.source.id || d.source) + '-' + (d.target.id || d.target));

labels.exit().remove();
linksEnter.attr('stroke', '#aaa').attr('stroke-width', 2);

const labelsEnter = labels.enter()
  .append('text')
  .attr('class', 'edge-label')
  .attr('font-size', 12)
  .attr('fill', '#e5e7eb')
  .attr('text-anchor', 'middle')
  .text(d => d.weight);

labelsEnter.merge(labels).text(d => d.weight);
  // N O D E S
  const nodes = nodeGroup.selectAll('g.node')
    .data(data.nodes, d => d.id);

  nodes.exit().remove();
  const nodesEnter = nodes.enter().append('g')
  .attr('class','node')
  .call(drag(simulation));

nodesEnter.append('circle').attr('r', 12);

nodesEnter.append('text')
  .attr('dy', -18)
  .text(d => d.id);

nodesEnter.append('title')
  .text(d => d.id);

  nodesEnter.on('click', (e, d) => {
  const algo = document.getElementById('algo').value;
  const srcSel = document.getElementById('source');
  const tgtSel = document.getElementById('target');

  if (algo === 'dijkstra') {
    tgtSel.value = d.id;  // sélectionne la cible
  } else {
    srcSel.value = d.id;  // met à jour la source
  }
});

  // T I C K
  simulation.on('tick', () => {
    linkGroup.selectAll('line')
      .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    labelGroup.selectAll('text.edge-label')
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2);
    nodeGroup.selectAll('g.node')
      .attr('transform', d => `translate(${d.x},${d.y})`);
  });

  // Auto-fit à la fin de la mise en place
  simulation.on('end', fit);
}

function drag(simulation){
  function dragstarted(event, d){
    if(!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
  }
  function dragged(event, d){
    d.fx = event.x; d.fy = event.y;
  }
  function dragended(event, d){
    if(!event.active) simulation.alphaTarget(0);
    d.fx = null; d.fy = null;
  }
  return d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended);
}

function clearHighlights(){
  d3.selectAll('.link').classed('highlight', false);
  d3.selectAll('.node').classed('highlight', false);
}

function highlightResult(result){
  clearHighlights();
  if(result.nodes_to_highlight){
    result.nodes_to_highlight.forEach(id => {
      d3.selectAll('.node').filter(d => d.id === id).classed('highlight', true);
    });
  }
  if(result.edges_to_highlight){
    result.edges_to_highlight.forEach(e => {
      d3.selectAll('.link').filter(d =>
        ((d.source.id||d.source)===e.source && (d.target.id||d.target)===e.target) ||
        ((d.source.id||d.source)===e.target && (d.target.id||d.target)===e.source)
      ).classed('highlight', true);
    });
  }
}
function renderResult(algo, data){
  clearResult();

  if(algo === 'bfs' || algo === 'dfs'){
    setSummary([
      ['Algorithme', algo.toUpperCase()],
      ['Taille du parcours', (data.order || []).length]
    ]);
    setChips(data.order || []);
  }

  if(algo === 'dijkstra'){
    setSummary([
      ['Algorithme', 'Dijkstra'],
      ['Coût total', data.cost != null ? data.cost : '—'],
      ['Longueur du chemin', (data.path || []).length]
    ]);
    setChips(data.path || []);
  }

  if(algo === 'kruskal'){
    setSummary([
      ['Algorithme', 'Kruskal (MST)'],
      ['Coût total', data.total != null ? data.total : '—'],
      ['Arêtes', (data.tree_edges || []).length]
    ]);
    const rows = (data.tree_edges || []).map(e => [e.source, e.target]);
    setTable(['Source (Par de)','Cible (Arrive sur)'], rows);
  }

  if(algo === 'prim'){
    setSummary([
      ['Algorithme', 'Prim (MST)'],
      ['Coût total', data.total != null ? data.total : '—'],
      ['Arêtes', (data.tree_edges || []).length]
    ]);
    const rows = (data.tree_edges || []).map(e => [e.source, e.target]);
    setTable(['Source (Par de)','Cible (Arrive sur)'], rows);
  }

  if(algo === 'bellman'){
    setSummary([
      ['Algorithme', 'Bellman–Ford'],
      ['Source', document.getElementById('source').value || '—']
    ]);
    if (data.error){
      setChips(['Cycle négatif détecté']);
    } else {
      const pairs = Object.entries(data.distances_from_source || {}).map(([k,v]) => [k, v]);
      setTable(['Noeud','Distance'], pairs);
    }
  }

  if(algo === 'floyd'){
    setSummary([
      ['Algorithme', 'Floyd–Warshall'],
      ['Paires totales', countFWPairs(data.distances)]
    ]);
    setFWTable(data.distances || {});
  }
}

function clearResult(){
  document.getElementById('summary')?.replaceChildren();
  document.getElementById('chips')?.replaceChildren();
  document.getElementById('thead')?.replaceChildren();
  document.getElementById('tbody')?.replaceChildren();
}

function setSummary(pairs){
  const box = document.getElementById('summary');
  if(!box) return;
  pairs.forEach(([k,v]) => {
    const row = document.createElement('div');
    row.className = 'kv';
    row.innerHTML = `<span class="k">${k}</span><span class="v">${v}</span>`;
    box.appendChild(row);
  });
}

function setChips(items){
  const c = document.getElementById('chips');
  if(!c) return;
  items.forEach(t => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = t;
    c.appendChild(chip);
  });
}

function setTable(headers, rows){
  const thead = document.getElementById('thead');
  const tbody = document.getElementById('tbody');
  if(!thead || !tbody) return;
  thead.innerHTML = `<tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr>`;
  tbody.innerHTML = rows.map(r => `<tr>${r.map(x=>`<td>${x}</td>`).join('')}</tr>`).join('');
}

function countFWPairs(dist){
  if(!dist) return 0;
  const nodes = Object.keys(dist);
  return nodes.length * nodes.length;
}

function setFWTable(dist){
  const nodes = Object.keys(dist || {});
  if(!nodes.length) return;
  setTable([''].concat(nodes), nodes.map(i => [i].concat(nodes.map(j => dist[i][j]))));
}


async function loadGraph(name = document.getElementById('graphSelect')?.value || 'fr_routes'){
  const res = await fetch('/api/graph?name=' + encodeURIComponent(name));
  const data = await res.json();
  renderGraph(data);

// ✅ mets à jour l’UI "orienté / non orienté"
  const flag = !!data.directed;
  const badge = document.getElementById('directedBadge');
  const ck    = document.getElementById('directedFlag');
  if (badge) badge.textContent = flag ? 'Orienté' : 'Non orienté';
  if (ck)    ck.checked = flag;

  const nodes = (data.nodes || []).map(n => n.id);
  const srcSel = document.getElementById('source');
  const tgtSel = document.getElementById('target');

  // Source : tous les sommets, pré-sélection = defaultSource
  fillSelect(srcSel, nodes, { selected: data.defaultSource });

  // Cible : tous les sommets, placeholder
  fillSelect(tgtSel, nodes, { placeholder: '— choisir une cible —' });
  tgtSel.value = ''; // laisse à choisir

  // si tu grises la cible selon l'algo, appelle updateControls() ici
  if (typeof updateControls === 'function') updateControls();
}

loadGraph();

document.getElementById('graphSelect').addEventListener('change', (e) => {
  loadGraph(e.target.value);
});

document.getElementById('runBtn').addEventListener('click', async () => {
  const graph  = document.getElementById('graphSelect')?.value; // ← une seule fois
  const algo   = document.getElementById('algo').value;
  const source = document.getElementById('source').value; // select
  const target = document.getElementById('target').value; // select

  // Cible requise pour Dijkstra
  if (algo === 'dijkstra' && !target) {
    document.getElementById('status').textContent = 'Choisis une cible (ville) pour Dijkstra';
    document.getElementById('target').classList.add('input-error');
    return;
  }
  document.getElementById('target').classList.remove('input-error');

  document.getElementById('status').textContent = '...';

  try {
    const res = await fetch('/api/run', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ graph, algo, source, target })
    });
    const out = await res.json();
    document.getElementById('status').textContent = res.ok ? 'OK' : 'Erreur';
    renderResult(algo, out);
    document.getElementById('output').textContent = JSON.stringify(out, null, 2);
    if (res.ok) highlightResult(out);
  } catch (err) {
    document.getElementById('status').textContent = 'Erreur réseau';
  }
});



const algoSel     = document.getElementById('algo');
const targetInput = document.getElementById('target');

function selectPlaceholder(sel){
  if (sel && sel.options.length && sel.options[0].value === '') {
    sel.selectedIndex = 0;
  }
}

function updateControls(){
  const needsTarget = (algoSel.value === 'dijkstra');
  targetInput.disabled = !needsTarget;
  if (!needsTarget) {
    selectPlaceholder(targetInput);
    targetInput.classList.remove('input-error');
  }
}

algoSel.addEventListener('change', updateControls);
document.addEventListener('DOMContentLoaded', updateControls);
updateControls();




document.getElementById('resetZoom').addEventListener('click', () => {
  svg.transition().duration(300).call(zoom.transform, d3.zoomIdentity);
});

function fillSelect(selectEl, values, {placeholder, selected} = {}){
  selectEl.replaceChildren();
  if (placeholder){
    const opt = document.createElement('option');
    opt.value = '';
    opt.textContent = placeholder;
    opt.disabled = true;
    opt.selected = !selected;
    selectEl.appendChild(opt);
  }
  values.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v;
    opt.textContent = v;
    if (selected && v === selected) opt.selected = true;
    selectEl.appendChild(opt);
  });
}
