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
        self.recips = {}

    def distance(self, name):
        for node in nodes:
            if node.name == name:
                break
        return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)

    def add_peer(self, name):
        if name not in self.peers and name != self.name:
            self.peers.append(name)
            self.recips[name] = 0

    def remove_peer(self, name):
        if name in self.peers:
            self.peers.remove(name)
            del self.recips[name]

    def flash(self):
        for name in self.peers:
            for node in nodes:
                if node.name == name:
                    self.recips[name] -= 1
                    if self.recips[name] < -10:
                        self.remove_peer(name)
                    else:
                        node.receive_flash(self.name, self.peers[0] if len(self.peers) else None)

    def receive_flash(self, sender, friend):
        if sender not in self.peers:
            self.add_peer(sender)
            self.peers.sort(key=lambda peer: self.distance(peer))
            if len(self.peers) > HOOD:
                self.remove_peer(self.peers[-1])
        if sender in self.peers:
            self.recips[sender] += 1
            if friend is not None and friend not in self.peers:
                self.add_peer(friend)
                self.peers.sort(key=lambda peer: self.distance(peer))
                if len(self.peers) > HOOD:
                    self.remove_peer(self.peers[-1])
            # bump

# create nodes
nodes = []
for i in range(NODES):
    node = Node(i)
    nodes.append(node)

# randomly assign peers
for node in nodes:
    for i in range(randint(0, HOOD)):
        node.add_peer(choice([peer.name for peer in nodes if node != peer]))

animator = LiveGraphAnimator()


def feed_data():

    n = 0

    for step in range(500):

        data = {}
        for node in nodes:
            data[node.name] = {'connections': [name for name in node.peers],
                               'x': node.x,
                               'y': node.y}

        animator.update_graph(data)
        time.sleep(0.1)  # simulate delay

        if step > 10:

            # flash
            node = nodes[n]
            node.flash()
            print(node.name, node.recips)
            n += 1
            n %= len(nodes)


# Run the data feeding in a separate thread
threading.Thread(target=feed_data, daemon=True).start()

animator.show()

