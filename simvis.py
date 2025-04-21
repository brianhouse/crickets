import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from collections import deque


class LiveGraphAnimator:
    def __init__(self, max_frames=100):
        self.frames = deque(maxlen=max_frames)  # Circular buffer of graph states
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.cmap = plt.cm.get_cmap('tab10')
        self.G = nx.DiGraph()
        self.ani = animation.FuncAnimation(
            self.fig,
            self._draw_frame,
            init_func=self._init_plot,
            interval=500,
            blit=False,
            cache_frame_data=False
        )
        self.pos = {}  # Persistent positions for each node

    def _init_plot(self):
        self.ax.clear()
        self.ax.set_title("Cricketnet - Live")
        # self.ax.axis("equal")
        self.ax.axis("off")  # cleaner look
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

    def _draw_frame(self, frame_idx):
        if not self.frames:
            return

        self.ax.clear()
        data = self.frames[-1]
        self.G.clear()

        # Add nodes and edges
        for node, node_data in data.items():
            self.G.add_node(node)
            for connection in node_data.get('connections', []):
                self.G.add_edge(node, connection)

        # Initialize positions for new nodes
        for node in self.G.nodes():
            if node not in self.pos:
                x = data[node].get('x', 5.0)
                y = data[node].get('y', 5.0)
                self.pos[node] = (x, y)

        # Smoothly update layout
        new_pos = nx.spring_layout(self.G, pos=self.pos, fixed=None, iterations=5, k=0.7)
        for node in self.pos:
            old_x, old_y = self.pos[node]
            new_x, new_y = new_pos[node]
            # Blend old and new positions for smooth motion
            self.pos[node] = (
                0.8 * old_x + 0.2 * new_x,
                0.8 * old_y + 0.2 * new_y,
            )

        # Colors
        node_colors = [self._get_node_color(node) for node in self.G.nodes()]
        edge_colors = []
        for u, v in self.G.edges():
            if self.G.has_edge(v, u):
                edge_colors.append('black')
            else:
                edge_colors.append(self._get_node_color(u))

        # Draw everything
        nx.draw_networkx_nodes(self.G, self.pos, ax=self.ax, node_color=node_colors, node_size=400)
        nx.draw_networkx_edges(self.G, self.pos, ax=self.ax, edge_color=edge_colors, arrows=False)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=8)

        self.ax.set_title("Cricketnet - Live")
        # self.ax.axis("off")

        # Get all positions as arrays
        x_vals = [pos[0] for pos in self.pos.values()]
        y_vals = [pos[1] for pos in self.pos.values()]

        # Add a little padding around the graph
        padding = 1.0
        self.ax.set_xlim(min(x_vals) - padding, max(x_vals) + padding)
        self.ax.set_ylim(min(y_vals) - padding, max(y_vals) + padding)



    def update_graph(self, new_data):
        """Call this method with new graph data (same format as before)."""
        self.frames.append(new_data)

    def show(self):
        plt.show()

    # def _get_node_color(self, node):
    #     # Assign a consistent color index for each node (hash-based)
    #     index = abs(hash(node)) % 10  # tab10 has 10 colors
    #     return self.cmap(index / 10)

    def _get_node_color(self, node):
        node_data = self.frames[-1].get(node, {})
        group = node_data.get("group", 0)
        # Handle null group (either None or string "null")
        if group is None or group == "null":
            return "#000000"
        if not hasattr(self, "_group_color_map"):
            self._group_color_map = {}
            self._next_color_index = 0
        if group not in self._group_color_map:
            self._group_color_map[group] = self.cmap(self._next_color_index % self.cmap.N)
            self._next_color_index += 1
        return self._group_color_map[group]
