#!venv/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

graph_data = {'8ONNqMB2': ['oqNJjLEq', 'seO296Jf', '4oO296Jf', 'sMI2jLEq', 'cvH2jLEq'], '4oO296Jf': ['seO296Jf', 'oqNJjLEq', '8ONNqMB2', 'sMI2jLEq', 'cvH2jLEq'], 'seO296Jf': ['4oO296Jf', 'oqNJjLEq', '8ONNqMB2', 'sMI2jLEq', 'cvH2jLEq'], 'oqNJjLEq': ['seO296Jf', '4oO296Jf', '8ONNqMB2', 'sMI2jLEq', 'cvH2jLEq'], 'cvH2jLEq': ['sMI2jLEq', 'oqNJjLEq', '8ONNqMB2', '4oO296Jf', 'seO296Jf'], 'sMI2jLEq': ['8ONNqMB2', 'oqNJjLEq', 'seO296Jf', '4oO296Jf', 'cvH2jLEq']}

# Create a Directed Graph
G = nx.DiGraph()

# Add edges from the dictionary
for node, connections in graph_data.items():
    for connection in connections:
        G.add_edge(node, connection)

# Assign a unique color to each node using a colormap
cmap = cm.get_cmap('tab10')
node_colors = {node: cmap(i / len(G.nodes())) for i, node in enumerate(G.nodes())}

# Check for symmetrical edges and assign edge colors
edge_colors = []
for edge in G.edges():
    if G.has_edge(edge[1], edge[0]):  # Check if the reverse edge exists
        edge_colors.append('black')  # Symmetrical edges are black
    else:
        edge_colors.append(node_colors[edge[0]])  # Non-symmetrical edges take the originating node's color

# Draw the directed graph using a spring layout
pos = nx.spring_layout(G)
plt.figure(figsize=(8, 6))

# Draw nodes with their assigned colors
nx.draw_networkx_nodes(G, pos, node_color=list(node_colors.values()), node_size=500)

# Draw edges with appropriate colors
nx.draw_networkx_edges(
    G, pos, edge_color=edge_colors, arrows=True,
    arrowstyle='-|>', arrowsize=15
)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_family='monospace')

plt.title("Cricketnet")
plt.show()