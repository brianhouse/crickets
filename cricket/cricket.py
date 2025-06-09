from util import *
from config import *

ALG.write(MOSENS)
FLASHES += randint(-FLASH_VARY, FLASH_VARY)


class Cricket(Node):

    def __init__(self):
        super().__init__()
        SND.duty(0)
        LED.off()
        STS.off()
        self.phase = random()
        self.pitch = randint(PITCH_LOW, PITCH_HIGH)
        self.hum = randint(HUM_LOW, HUM_HIGH)
        self.t_previous = ticks_ms()
        self.paused = False
        self.active = False
        self.group = None
        self.group_t = None
        self.flashes = 0
        O.print("##", self.name, "##")
        O.print("CHANNEL", self.channel)

    async def run(self):
        try:
            SND.duty(0)
            LED.off()
            STS.on()
            await asyncio.sleep(4)
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
                self.deactivate()
                LED.on()
                await asyncio.sleep(1)
                continue
            else:
                LED.off()
            try:
                await asyncio.sleep_ms(1)
                t = ticks_ms()
                t_elapsed = ticks_diff(t, self.t_previous)
                if t_elapsed >= TICK:
                    self.t_previous = t
                    error = abs(t_elapsed - TICK)
                    if error > 15:  # perceptibility
                        O.print("*", error)
                    O.reset()
                    self.phase = min(self.phase + (t_elapsed / 1000), 1.0)
                    if self.active and self.flashes == FLASHES:
                        O.print("REACHED FLASHES")
                        self.deactivate()
                    if not self.active and self.group_t and ticks_diff(t, self.group_t) > GROUP_TIME * 1000:
                        O.print("GROUP EXPIRED")
                        self.group = None
                        self.group_t = None
                    self.look()
                    self.listen()
                    if self.capacitor >= 1.0:
                        self.flash()
            except Exception as e:
                if DEBUG:
                    raise e
                else:
                    O.print(e)

    def look(self):
        if not MOTION:
            return
        if not self.active and PIR.value():
            self.activate()
            for neighbor_name in get_neighbors(self.name)[:ACT_HOOD]:
                self.send("activate NOP NOP", neighbor_name)

    def listen(self):
        for sender, message in self.receive():
            O.print("GOT", message, "from", sender)
            try:
                kind, sender_group, group_list = message.split(" ")
            except Exception as e:
                O.print(f"BAD ({e}): \"{message}\"")
                continue
            if kind == "group":
                if not self.active:
                    O.print("GROUP", sender_group)
                    self.group = sender_group
                    self.group_t = ticks_ms()
            elif kind == "activate":
                if not self.active:
                    self.activate()
            elif kind == "flash":
                if self.active:
                    if sender_group == self.group:
                        self.bump()
                    else:
                        O.print("WRONG GROUP")
                else:
                    O.print("NOT ACTIVE")

    def spontaneous(self):
        if not self.active and random() < SPONTANEOUS:
            O.print("SPONTANEOUS")
            self.activate()
            for neighbor_name in get_neighbors(self.name)[:SPON_HOOD]:
                self.send("activate NOP NOP", neighbor_name)

    def activate(self):
        O.print("ACTIVATE")
        self.active = True
        self.flashes = 0
        self.phase = 1.0
        if self.group is None:
            O.print("STARTING GROUP", self.name)
            self.group = self.name
            self.group_t = ticks_ms()
            self.send_all(f"group {self.group} NOP")

    def deactivate(self):
        O.print("DEACTIVATE")
        self.active = False
        self.group = None
        self.group_t = None
        self.phase = random()

    def send_all(self, message):
        O.print("SEND", message)
        super().send(message)

    def send(self, message, peer_name):
        peer = Peer.find(name=peer_name)
        O.print("SEND", message, peer)
        try:
            super().add_peer(peer.bin_mac)
        except Exception:
            pass
        try:
            super().send(message, peer)
        except Exception as e:
            O.print(e)

    def flash(self):
        O.print("FLASH")
        self.spontaneous()
        self.phase = 0.0
        if self.active:
            self.flashes += 1
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

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value
        self._capacitor = self.f(value)

    @property
    def capacitor(self):
        return self._capacitor

    @capacitor.setter
    def capacitor(self, value):
        self._capacitor = value
        self._phase = self.f_inv(value)

    def f(self, x):
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y):
        return (2 / math.pi) * math.asin(y)


