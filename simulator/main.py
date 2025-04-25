#!venv/bin/python

import json, math, time, threading, random
from random import choice, randint
from vis import LiveGraphAnimator


NODES = 100
MAX_HOOD = 8
MIN_HOOD = 3
FRIEND_LINK = .2
GROUP_LEADER = .2
SEVER = -4

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
        if random.random() < GROUP_LEADER:
            self.group = "group_" + self.name
        neighbors = list(nodes)
        neighbors.sort(key=lambda neighbor: self.distance(neighbor.name))
        i = 0
        while len(self.peers) < MIN_HOOD:
            self.add_peer(neighbors[i].name)
            i += 1

    def distance(self, name):
        for node in nodes:
            if node.name == name:
                return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)
        return 1000

    def add_peer(self, name, friend=False):
        if len(self.peers) >= MAX_HOOD:
            return
        if name not in self.peers and name != self.name:
            self.peers.append(name)
            self.recips[name] = 0
            self.peers.sort(key=lambda peer: self.distance(peer) if not friend else 1000)  # not exact, because this will refresh faster than the reality
            if len(self.peers) > MAX_HOOD:
                self.remove_peer(self.peers[-1])

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
                    if self.recips[name] < SEVER:
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
                if friend not in self.peers and random.random() < FRIEND_LINK:
                    self.add_peer(friend, True)
                # bump
            else:
                self.remove_peer(sender)


# create nodes
nodes = []
for i in range(NODES):
    node = Node(i)
    nodes.append(node)
for node in nodes:
    for i in range(MIN_HOOD):
        other = choice([other for other in nodes if other != node])
        node.add_peer(other.name)


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

