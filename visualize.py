#!venv/bin/python

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from util import *

with open("peers.json") as f:
    graph_data = json.loads(f.read())

G = nx.DiGraph()
for node, node_data in graph_data.items():
    G.add_node(node)
    for connection in node_data.get('peers', []):
        G.add_edge(node, connection)

# assign colors
cmap = matplotlib.colormaps.get_cmap('tab10')
# node_colors = {node: cmap(i / len(G.nodes())) for i, node in enumerate(G.nodes())}

_group_color_map = {}
_next_color_index = 0

def _get_node_color(node):
    global _next_color_index
    node_data = graph_data.get(node, {})
    group = node_data.get("group", 0)
    # Handle null group (either None or string "null")
    if group is None or group == "null":
        return "#cccccc"
    if group not in _group_color_map:
        _group_color_map[group] = cmap(_next_color_index % cmap.N)
        _next_color_index += 1
    return _group_color_map[group]

node_colors = {node: _get_node_color(node) for node in G.nodes()}

# symmetrical edges get black / otherwise get the originating node color
edge_colors = []
for edge in G.edges():
    if G.has_edge(edge[1], edge[0]):
        edge_colors.append('black')
    else:
        edge_colors.append(node_colors[edge[0]])

# draw nodes and edges with their assigned colors
pos = nx.spring_layout(G, 1)
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_color=list(node_colors.values()), node_size=900)
nx.draw_networkx_edges(
    G, pos, edge_color=edge_colors, arrows=False
)

# labels
nx.draw_networkx_labels(G, pos, font_size=6, font_color='black', font_weight='bold', font_family='monospace')

plt.title("Cricketnet")
plt.show()