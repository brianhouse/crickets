from util import *
from config import *


class Cricket(Node):

    def __init__(self):
        super().__init__()
        SND.duty(0)
        LED.off()
        STS.off()
        self.phase = random()
        self.capacitor = self.f(self.phase)
        self.pitch = randint(PITCH_LOW, PITCH_HIGH)
        self.hum = randint(HUM_LOW, HUM_HIGH)
        self.t_previous = ticks_ms()
        self.peers = []
        self.group = "null"
        self.motion = 0
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
                    self.listen()
                    if self.capacitor >= 1.0:
                        self.flash()
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
        if STATUS:
            STS.on()
        await asyncio.sleep_ms(randint(0, 1000))  # mess up the oscillator
        self.clear_peers()
        neighbors = self.scan(RANGE, True)  # sorting
        if len(neighbors):
            for i in range(MAX_HOOD):
                if i < len(neighbors):
                    self.add_peer(neighbors[i])
        if STATUS:
            STS.off()
        if HUM:
            SND.duty(0)
        O.print("--> DONE")

    def listen(self):
        action = None
        for sender, message in self.receive():
            O.print("GOT", message, "from", sender)
            try:
                peers = []
                action, sender_group, peer_names = message.split(" ")
                for peer_name in peer_names.split(","):
                    if not len(peer_name) or peer_name == "NOP" or peer_name == self.name:
                        continue
                    peers.append(Peer.find(name=peer_name))
            except Exception as e:
                print(f"BAD ({e}): \"{message}\"")
                continue
        if action == "flash":
            if sender_group != "null":
                if self.group == "null":
                    self.group = sender_group
                if sender_group == self.group:
                    self.add_peer(sender)
                    for peer in peers:
                        self.add_peer(peer)
                else:
                    self.remove_peer(sender)
                    self.send("break", sender)
                    for peer in peers:
                        self.remove_peer(peer)
                        self.send("break", peer)
            else:
                self.add_peer(sender)
            self.cut_peers()
            self.bump()
        elif action == "break":
            self.remove_peer(sender)

    def add_peer(self, peer):
        if len(self.peers) >= 20 or peer in self.peers or peer.name == self.name:
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

    def cut_peers(self):
        self.peers.sort(key=lambda peer: (peer.rssi is not None, peer.rssi), reverse=True)
        while len(self.peers) > MAX_HOOD:
            O.print("CUT", self.peers[-1])
            self.remove_peer(self.peers[-1])

    def send(self, action, peer=None):
        if peer is None:
            O.print("SEND", self.peers)
            if len(self.peers):
                super().send(f"{action} {self.group} {",".join([peer.name for peer in self.peers])}")
        else:
            O.print("SEND", peer)
            super().send(f"{action} {self.group} NOP", peer)

    def flash(self):
        O.print("FLASH")
        self.phase = 0.0
        self.capacitor = 0.0
        if BLINK:
            LED.on()
        if STATUS:
            STS.on()
        self.send("flash")
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
            return
        O.print("BUMP")
        self.capacitor = min(self.capacitor + (BUMP / 1000), 1.0)
        self.phase = self.f_inv(self.capacitor)

    def f(self, x):
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y):
        return (2 / math.pi) * math.asin(y)
