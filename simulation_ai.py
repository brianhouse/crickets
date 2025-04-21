#!venv/bin/python

import json, math, time, threading, random
from random import choice, randint
from simvis import LiveGraphAnimator


NODES = 20
HOOD = 5
RANGE = 3

STRENGTHEN_RATE = 0.1
WEAKEN_RATE = 0.1
DROP_THRESHOLD = 0.3


def jaccard_similarity(set1, set2):
    if not set1 or not set2:
        return 0.0
    return len(set(set1) & set(set2)) / len(set(set1) | set(set2))


class Node():

    def __init__(self, name):
        self.name = str(name)
        self.x = name // 5
        self.y = name % 4
        self.peers = []
        self.peer_strength = {}

    def distance(self, peer):
        return math.sqrt((self.x - peer.x)**2 + (self.y - peer.y)**2)

    def add_peer(self, name):
        if name not in self.peers:
            self.peers.append(name)
            if name not in self.peer_strength:
                self.peer_strength[name] = 1.0

    def remove_peer(self, name):
        if name in self.peers:
            self.peers.remove(name)
            # del self.peer_strength[name]

    def flash(self):
        for name in self.peers:
            for node in nodes:
                if node.name == name:
                    node.receive_flash(self.name, [name for name in self.peers])

    def receive_flash(self, sender, sender_peers):
        if len(self.peers) < HOOD and sender not in self.peers:
            self.add_peer(sender)
        if sender in self.peers:
            self.update_link_strength(sender, sender_peers)
            if len(self.peers) > 1 and len(sender_peers) > 1:
                self.remove_peer(choice([name for name in self.peers if name != sender]))
                self.add_peer(choice([name for name in sender_peers if name != self.name]))
            # bump

    def update_link_strength(self, peer, peer_peers):
        if peer not in self.peer_strength:
            return

        similarity = jaccard_similarity(self.peers, peer_peers)

        if similarity > 0.3:
            self.peer_strength[peer] = min(1.0, self.peer_strength[peer] + STRENGTHEN_RATE)
        else:
            self.peer_strength[peer] = max(0.0, self.peer_strength[peer] - WEAKEN_RATE)

        if self.peer_strength[peer] < DROP_THRESHOLD:
            self.remove_peer(peer)


# create nodes
nodes = []
for i in range(NODES):
    node = Node(i)
    nodes.append(node)

# randomly assign peers
for node in nodes:
    for i in range(randint(0, HOOD)):
        node.add_peer(choice([peer.name for peer in nodes if node.distance(peer) < RANGE and node != peer]))

animator = LiveGraphAnimator()


def feed_data():

    # n = 0

    for step in range(500):
        print(step)

        data = {}
        for node in nodes:
            data[node.name] = {'connections': [name for name in node.peers],
                               'x': node.x,
                               'y': node.y}

        animator.update_graph(data)
        time.sleep(0.1)  # simulate delay

        # flash
        for node in nodes:
            node.flash()
            print(node.name, node.peer_strength)
        # n += 1
        # n %= len(nodes)


# Run the data feeding in a separate thread
threading.Thread(target=feed_data, daemon=True).start()

animator.show()

