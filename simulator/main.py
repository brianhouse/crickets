#!venv/bin/python

import json, math, time, threading, random
from random import choice, randint
from vis import LiveGraphAnimator


NODES = 100
MAX_HOOD = 10
INIT_HOOD = 5
MIN_HOOD = 3


class Node():

    def __init__(self, name):
        self.name = str(name)
        self.x = name // 10
        self.y = name % 10
        self.peers = []
        self.group = "null"
        self.recips = {}

    def look(self):
        self.group = "null"
        if random.random() < .2:
            self.group = "group_" + self.name
        neighbors = list(nodes)
        neighbors.sort(key=lambda neighbor: self.distance(neighbor.name))
        i = 0
        while len(self.peers) < INIT_HOOD:
            self.add_peer(neighbors[i].name)
            i += 1

    def distance(self, name):
        for node in nodes:
            if node.name == name:
                return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)
        return 1000

    def add_peer(self, name):
        if len(self.peers) >= MAX_HOOD:
            return
        if name not in self.peers and name != self.name:
            self.peers.append(name)
            self.recips[name] = 0

    def remove_peer(self, name):
        if name in self.peers:
            self.peers.remove(name)
            del self.recips[name]

    def flash(self):
        if len(self.peers) < MIN_HOOD:
            self.look()
        for name in self.peers:
            for node in nodes:
                if node.name == name:
                    self.recips[name] -= 1
                    if self.recips[name] < -3:
                        self.remove_peer(name)
                    else:
                        friend = choice(self.peers)
                        node.receive_flash(self.name, self.group, friend)

    def receive_flash(self, sender, sender_group, friend):

        if sender in self.peers:
            self.recips[sender] += 1

        # both unassigned
        if self.group == "null" and sender_group == "null":
            # self.add_peer(sender)
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
                if friend not in self.peers and random.random() < .2:
                    self.add_peer(friend)
                # bump
            else:
                self.remove_peer(sender)


# create nodes
nodes = []
for i in range(NODES):
    node = Node(i)
    nodes.append(node)
# for i in range(2):
#     node = choice(nodes)
#     node.group = "group_" + node.name


animator = LiveGraphAnimator()


def feed_data():

    i = 0
    party = []

    while True:

        data = {}
        for node in nodes:
            data[node.name] = {'connections': [name for name in node.peers],
                               'x': node.x,
                               'y': node.y,
                               'group': node.group
                               }

        animator.update_graph(data)
        time.sleep(1 / 100)

        i += 1

        if True:

            if not len(party):
                party = nodes[:]
                random.shuffle(party)
                print("blink")

            # flash
            node = party.pop()
            node.flash()
            # print(node.name, node.peers, node.group)


# Run the data feeding in a separate thread
threading.Thread(target=feed_data, daemon=True).start()

animator.show()

