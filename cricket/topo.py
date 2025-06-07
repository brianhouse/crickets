import math


# OCTANT 1 #


CHANNEL = 8

grid = {
    "AB7MqMB2": (1, 2, 3),  # tester

    "0WpyvsCF": (1, 2, 3),
    "ESnyvsCF": (1, 2, 3),
    "cm3MqMB2": (1, 2, 3),
    "g96MqMB2": (1, 2, 3),
    "cAI2jLEq": (1, 2, 3),
    "87H2jLEq": (1, 2, 3),
    "k3J6JxI1": (1, 2, 3),
    "89nyvsCF": (1, 2, 3),
    "cVpyvsCF": (1, 2, 3),
    "o_7MqMB2": (1, 2, 3),
    "YhGNqMB2": (1, 2, 3),
    "w0ENqMB2": (1, 2, 3),
    "0SnyvsCF": (1, 2, 3),
    "wi8MqMB2": (1, 2, 3),
    "AbpyvsCF": (1, 2, 3),
    "w8XNqMB2": (1, 2, 3),
    "k8H2jLEq": (1, 2, 3),
    "QdpyvsCF": (1, 2, 3),
    "EHJNqMB2": (1, 2, 3),
    "MM-MqMB2": (1, 2, 3),
    "sK6MqMB2": (1, 2, 3),
    "ceNNqMB2": (1, 2, 3),
    "0bpyvsCF": (1, 2, 3),
    "Ig9MqMB2": (1, 2, 3),
    "k-myvsCF": (1, 2, 3),
    "0pNJjLEq": (1, 2, 3),
    "gIYNqMB2": (1, 2, 3),
    "oW0MqMB2": (1, 2, 3),
    "gnGNqMB2": (1, 2, 3),
    "A_5MqMB2": (1, 2, 3),
    "cvJNqMB2": (1, 2, 3),
    "kj4MqMB2": (1, 2, 3),
    "4CONqMB2": (1, 2, 3),
}


def get_neighbors(name):
    try:
        x1, y1, z1 = grid[name]
        distances = []
        for key in grid:
            if key == name:
                continue
            x2, y2, z2 = grid[key]
            distances.append((key, math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)))
        distances.sort(key=lambda d: d[1])
        return [distance[0] for distance in distances]
    except KeyError as e:
        print(e)

