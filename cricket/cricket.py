from util import *
from config import *


class Cricket(Node):

    def __init__(self):
        Node.__init__(self)
        SND.duty(0)
        self.phase = random()
        self.capacitor = self.f(self.phase)
        self.pitch = randint(PITCH_LOW, PITCH_HIGH)
        self.hum = randint(HUM_LOW, HUM_HIGH)
        self.t_previous = ticks_ms()
        self.group = "null"
        self.peers = []
        O.print(f"## {self.name} ##")

    async def run(self):
        await asyncio.sleep_ms(randint(1000, 3000))
        self.look()
        self.receive()  # clear messages
        self.t_previous = ticks_ms()
        while True:
            # try:
                t = ticks_ms()
                t_elapsed = ticks_diff(t, self.t_previous)
                if t_elapsed >= TICK:
                    error = abs(t_elapsed - TICK)
                    # O.print("TICK", t_elapsed)
                    if error > 15:  # perceptibility
                        O.print("*", error)
                    O.reset()
                    self.t_previous = t
                    self.phase = min(self.phase + (t_elapsed / 1000), 1.0)
                    self.capacitor = self.f(self.phase)
                    if self.capacitor >= 1.0:
                        await self.flash()
                    # O.print("MEM", gc.mem_free())
                    self.listen()
                    if len(self.peers) < MIN_HOOD:
                        O.print("LONELY")
                        self.look()
                    gc.collect()
                await asyncio.sleep_ms(1)
            # except Exception as e:
            #     O.print(e)

    def look(self):
        self.group = "null"
        if random() < GROUP_LEADER:
            self.group = self.name
            O.print("LEADER")
        O.print("LOOK...")
        if HUM:
            SND.duty(0)
            SND.duty(512)
            SND.freq(self.hum)
        self.clear_peers()
        neighbors = self.scan()
        if len(neighbors):
            for i in range(MIN_HOOD):
                if i < len(neighbors) and neighbors[i].rssi > RANGE:
                    self.add_peer(neighbors[i])
        if HUM:
            SND.duty(0)
        O.print("--> DONE")

    def listen(self):
        messages = self.receive()
        for message in messages:
            sender, message = message
            O.print("GOT", message, "from", sender)
            _, sender_group, friend = message.split(" ")

            if sender in self.peers:
                sender.recip = 0

            # both unassigned
            if self.group == "null" and sender_group == "null":
                if self.bump():
                    return

            # self unassigned, sender assigned
            elif self.group == "null":
                self.group = sender_group
                self.add_peer(sender)
                if self.bump():
                    return

            # self assigned, sender unassigned
            elif sender_group == "null":
                self.add_peer(sender)

            # both have groups assigned
            else:
                if self.group == sender_group:
                    self.add_peer(sender)
                    if friend != "null" and friend != self.name and random() < FRIEND_LINK:
                        self.add_peer(Peer.find(name=friend))
                    if self.bump():
                        return
                else:
                    self.remove_peer(sender)

    def cull_peers(self):

        # distance
        for peer in self.peers:
            if peer.rssi is not None and peer.rssi < RANGE:
                O.print("DIS", peer)
                self.remove_peer(peer)

        # if more than MAX_HOOD peers and a last peer has an rssi, remove it (and avoid sort())
        # (recips will take care of it if there's peers w/o an rssi)
        if len(self.peers) > MAX_HOOD:
            furthest = None
            for peer in self.peers:
                if peer.rssi is not None and (furthest is None or peer.rssi < furthest.rssi):
                    furthest = peer
            if furthest is not None:
                O.print("CUT", furthest)
                self.remove_peer(furthest)

    def add_peer(self, peer):
        if peer in self.peers:
            return
        O.print(f"ADD {peer}")
        self.peers.append(peer)
        self.mesh.add_peer(peer.bin_mac)

    def remove_peer(self, peer):
        if peer in self.peers:
            O.print(f"REMOVE {peer}")
            try:
                self.peers.remove(peer)
                self.mesh.del_peer(peer.bin_mac)
            except Exception as e:
                O.print(e)

    def clear_peers(self):
        for peer in self.peers:
            try:
                self.mesh.del_peer(peer.bin_mac)
            except Exception as e:
                O.print(e)
        self.peers.clear()

    async def send(self):
        O.print("SEND", self.peers)
        for peer in self.peers:
            peer.recips -= 1
            if peer.recips < SEVER:
                O.print("GHOST", peer)
                self.remove_peer(peer)
        friend = choice(self.peers).name if len(self.peers) else "null"
        if len(self.peers):
            await Node.send(self, f"flash {self.group} {friend}")

    async def flash(self):
        O.print("FLASH")
        self.phase = 0.0
        self.capacitor = 0.0
        if BLINK:
            LED.on()
        if STATUS:
            STS.on()
        self.cull_peers()
        await self.send()
        if CHIRP:
            SND.duty(512)
            SND.freq(self.pitch * 2)
        sleep_ms(30)
        if CHIRP:
            SND.freq(self.pitch)
        sleep_ms(30)
        if CHIRP:
            SND.duty(0)
        if BLINK:
            LED.off()
        if STATUS:
            STS.off()

    def bump(self):
        if self.phase * 1000 < REST:
            O.print("REST")
            return False
        O.print("BUMP")
        self.capacitor = min(self.capacitor + BUMP, 1.0)
        self.phase = self.f_inv(self.capacitor)
        if self.capacitor >= 1.0:
            self.flash()
        return True

    def f(self, x):
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y):
        return (2 / math.pi) * math.asin(y)

