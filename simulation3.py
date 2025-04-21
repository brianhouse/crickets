#!venv/bin/python

import json, math, time, threading, random
from random import choice, randint
from simvis import LiveGraphAnimator


NODES = 16
HOOD = 3
RANGE = 3


class Node():

    def __init__(self, name):
        self.name = str(name)
        self.x = name // 4
        self.y = name % 4
        self.peers = []
        self.group = "null"

    def distance(self, name):
        for node in nodes:
            if node.name == name:
                return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)
        return 1000

    def add_peer(self, name):
        if name not in self.peers and name != self.name:
            self.peers.append(name)

    def remove_peer(self, name):
        if name in self.peers:
            self.peers.remove(name)

    def flash(self):
        for name in self.peers:
            for node in nodes:
                if node.name == name:
                    node.receive_flash(self.name, self.group)

    def receive_flash(self, sender, sender_group):

        # both unassigned
        if self.group == "null" and sender_group == "null":
            pass

        # self unassigned, sender assigned
        elif self.group == "null":
            self.group = sender_group
            self.add_peer(sender)
            # bump

        # self assigned, sender unassigned
        elif sender_group == "null":
            self.add_peer(sender)

        # both have groups assigned
        else:
            if self.group == sender_group:
                if sender not in self.peers:
                    self.add_peer(sender)
                # bump
            else:
                self.remove_peer(sender)


# create nodes
nodes = []
for i in range(NODES):
    node = Node(i)
    nodes.append(node)
for i in range(2):
    node = choice(nodes)
    node.group = "group_" + node.name


# randomly assign peers
for node in nodes:
    neighbors = list(nodes)
    neighbors.sort(key=lambda neighbor: node.distance(neighbor.name))
    i = 0
    while len(node.peers) < HOOD:
        node.add_peer(neighbors[i].name)
        i += 1

animator = LiveGraphAnimator()


def feed_data():

    n = 0
    i = 0

    while True:

        data = {}
        for node in nodes:
            data[node.name] = {'connections': [name for name in node.peers],
                               'x': node.x,
                               'y': node.y,
                               'group': node.group
                               }

        animator.update_graph(data)
        time.sleep(1 / 30)  # simulate delay

        i += 1

        if i % 3 == 0:

            # flash
            node = nodes[n]
            node.flash()
            print(node.name, node.peers, node.group)
            n += 1
            n %= len(nodes)


# Run the data feeding in a separate thread
threading.Thread(target=feed_data, daemon=True).start()

animator.show()

