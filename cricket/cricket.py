from util import *
from config import *

ALG.write(MOSENS)


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
        self.group = None
        self.paused = False
        O.print(f"## {self.name} ##")

    async def run(self):
        try:
            STS.on()
            await asyncio.sleep_ms(randint(1000, 3000))
            self.receive()  # clear messages
            STS.off()
        except Exception as e:
            if DEBUG:
                raise e
            else:
                O.print(e)
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
                    if MOTION:
                        if PIR.value():
                            print("MOTION")
                            await self.look()
                            continue
                    if self.group is not None and len(self.peers) < MIN_HOOD:
                        print("BELOW MIN")
                        self.clear_peers()
                        self.group = None
                        STS.off()
                    self.listen()
                    if self.capacitor >= 1.0:
                        self.flash()
                    # O.print("MEM", gc.mem_free())
                    gc.collect()
            except Exception as e:
                if DEBUG:
                    raise e
                else:
                    O.print(e)

    async def look(self):
        O.print("LEADER...")
        self.group = self.name
        if HUM:
            SND.duty(0)
            SND.duty(512)
            SND.freq(self.hum)
        STS.on()
        await asyncio.sleep_ms(2000)  # needs to be at least 2s for the PIR
        await asyncio.sleep_ms(randint(0, 1000))  # mess up the oscillator
        self.clear_peers()
        neighbors = self.scan(RANGE, True)  # sorting
        if len(neighbors):
            for i in range(MAX_HOOD):
                if i < len(neighbors):
                    self.add_peer(neighbors[i])
        self.send_all(f"group {self.group} {"*".join([peer.name for peer in self.peers])}")
        self.receive()  # clear messages
        if not STATUS or (self.group != self.name):
            STS.off()
        if HUM:
            SND.duty(0)
        O.print("--> DONE")

    def listen(self):
        for sender, message in self.receive():
            O.print("GOT", message, "from", sender)
            try:
                kind, sender_group, group_list = message.split(" ")
            except Exception as e:
                O.print(f"BAD ({e}): \"{message}\"")
                continue
            if kind == "group":
                O.print("GROUP", sender_group)
                self.group = sender_group
                STS.off()
                self.clear_peers()
                self.add_peer(sender)
                for name in group_list.split("*"):
                    self.add_peer(Peer.find(name))
            elif kind == "reject":
                O.print("REJECTED")
                self.remove_peer(sender)
            elif kind == "flash":
                if sender_group == self.group:
                    if sender.rssi < RANGE:
                        O.print("REJECT TOO FAR")
                        self.add_peer(sender)
                        self.send(f"reject {self.group} NOP", sender)
                        self.remove_peer(sender)
                    self.bump()
                else:
                    O.print("REJECT OTHER GROUP")
                    self.add_peer(sender)
                    self.send(f"reject {self.group} NOP", sender)
                    self.remove_peer(sender)

    def add_peer(self, peer):
        if peer in self.peers or peer.name == self.name:
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

    def send_all(self, message):
        O.print("SEND", self.peers, message)
        if len(self.peers):
            super().send(message)

    def send(self, message, peer):
        O.print("SEND", peer, message)
        super().send(message, peer)

    def flash(self):
        O.print("FLASH")
        self.phase = 0.0
        self.capacitor = 0.0
        if self.group is not None:
            if BLINK:
                LED.on()
            else:
                STS.on()
            self.send_all(f"flash {self.group} NOP")
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
            else:
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


