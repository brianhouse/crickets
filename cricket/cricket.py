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
        self.capacitor = self.f(self.phase)
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
            await asyncio.sleep(2)
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
                self.reset()
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
                    self.capacitor = self.f(self.phase)
                    if self.active and self.flashes == FLASHES:
                        O.print("REACHED FLASHES")
                        self.active = False
                        self.group = None
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
            O.print("ACTIVATE")
            self.active = True
            self.flashes = 0
            self.phase = 1.0
            self.capacitor = self.f(self.phase)
            if self.group is None:
                O.print("STARTING GROUP", self.name)
                self.group = self.name
                self.group_t = ticks_ms()
                self.send_all(f"group {self.group} NOP")

    # def look(self):
    #     O.print("LOOK...")
    #     self.group = self.name
    #     self.clear_peers()
    #     for neighbor_name in get_neighbors(self.name)[:MAX_HOOD]:
    #         self.add_peer(Peer.find(neighbor_name))
    #     self.send_all(f"group {self.group} {"*".join([peer.name for peer in self.peers])}")
    #     O.print("CLEAR MESSAGES")
    #     self.receive()  # clear messages
    #     O.print("--> DONE")

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
            elif kind == "flash":
                if self.active:
                    if sender_group == self.group:
                        self.bump()
                    else:
                        O.print("WRONG GROUP")
                else:
                    O.print("NOT ACTIVE")

    def send_all(self, message):
        O.print("SEND", message)
        super().send(message)

    def flash(self):
        O.print("FLASH")
        self.phase = 0.0
        self.capacitor = 0.0
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
        self.phase = self.f_inv(self.capacitor)

    def f(self, x):
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y):
        return (2 / math.pi) * math.asin(y)


