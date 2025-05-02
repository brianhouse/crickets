from util import *
from config import *


class Cricket(Node):

    def __init__(self):
        super().__init__()
        SND.duty(0)
        self.phase = random()
        self.capacitor = self.f(self.phase)
        self.pitch = randint(PITCH_LOW, PITCH_HIGH)
        self.hum = randint(HUM_LOW, HUM_HIGH)
        self.t_previous = ticks_ms()
        self.group = "null"
        self.peers = []
        self.paused = False
        O.print(f"## {self.name} ##")

    async def run(self):
        await asyncio.sleep_ms(randint(1000, 3000))
        await self.look()
        self.receive()  # clear messages
        self.t_previous = ticks_ms()
        while True:
            if self.paused:
                LED.on()
                STS.on()
                await asyncio.sleep(1)
                continue
            try:
                await asyncio.sleep_ms(1)
                t = ticks_ms()
                t_elapsed = ticks_diff(t, self.t_previous)
                if t_elapsed >= TICK:
                    self.t_previous = t
                    error = abs(t_elapsed - TICK)
                    # O.print("TICK", t_elapsed)
                    if error > 15:  # perceptibility
                        O.print("*", error)
                    O.reset()
                    self.phase = min(self.phase + (t_elapsed / 1000), 1.0)
                    self.capacitor = self.f(self.phase)
                    if self.capacitor >= 1.0:
                        self.flash()
                        continue
                    # O.print("MEM", gc.mem_free())
                    self.listen()
                    if len(self.peers) < MIN_HOOD:
                        O.print("LONELY")
                        await self.look()
                    gc.collect()
            except Exception as e:
                if DEBUG:
                    raise e
                else:
                    O.print(e)

    async def look(self):
        self.group = "null"
        if random() < GROUP_LEADER:
            self.group = self.name
            O.print("LEADER")
        O.print("LOOK...")
        if HUM:
            SND.duty(0)
            SND.duty(512)
            SND.freq(self.hum)
        await asyncio.sleep_ms(100)  # give connection a chance
        self.clear_peers()
        neighbors = self.scan(RANGE)
        if len(neighbors):
            for i in range(MIN_HOOD):
                if i < len(neighbors):
                    self.add_peer(neighbors[i])
        if HUM:
            SND.duty(0)
        O.print("--> DONE")

    def listen(self):
        for sender, message in self.receive():
            O.print("GOT", message, "from", sender)
            if sender.rssi < RANGE:
                print("TOO FAR")
                continue

            _, sender_group, friend_name = message.split(" ")

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
                    if friend_name != "null" and friend_name != self.name and random() < FRIEND_LINK:
                        friend = Peer.find(name=friend_name)
                        if friend.rssi is None or friend.rssi >= RANGE:
                            self.add_peer(friend)
                    if self.bump():
                        return
                else:
                    self.remove_peer(sender)


    def cull_peers(self):

        # anybody ghosted?
        for peer in self.peers:
            peer.recips -= 1
            if peer.recips < SEVER:
                O.print("GHOST", peer)
                self.remove_peer(peer)

        # really too far
        for peer in self.peers:
            if peer.rssi is not None and peer.rssi < RANGE:
                O.print("DIS", peer)
                self.remove_peer(peer)

        # if more than MAX_HOOD peers and a last peer has an rssi, remove it (and avoid sort())
        # (recips will take care of it if there's peers w/o an rssi)
        while len(self.peers) > MAX_HOOD:
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
        try:
            super().add_peer(peer.bin_mac)
        except Exception as e:
            O.print(e)

    def remove_peer(self, peer):
        if peer in self.peers:
            O.print(f"REMOVE {peer}")
            self.peers.remove(peer)
            try:
                super().remove_peer(peer.bin_mac)
            except Exception as e:
                O.print(e)

    def clear_peers(self):
        for peer in self.peers:
            try:
                super().remove_peer(peer.bin_mac)
            except Exception as e:
                O.print(e)
        self.peers.clear()

    def send(self):
        O.print("SEND", self.peers)
        if len(self.peers):
            friend = choice(self.peers).name
            super().send(f"flash {self.group} {friend}")

    def flash(self):
        O.print("FLASH")
        self.phase = 0.0
        self.capacitor = 0.0
        if BLINK:
            LED.on()
        if STATUS:
            STS.on()
        self.cull_peers()
        self.send()
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
        self.capacitor = min(self.capacitor + (BUMP / 1000), 1.0)
        self.phase = self.f_inv(self.capacitor)
        if self.capacitor >= 1.0:
            self.flash()
            return True
        return False

    def f(self, x):
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y):
        return (2 / math.pi) * math.asin(y)

