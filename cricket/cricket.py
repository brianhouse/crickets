import uasyncio as asyncio
from config import *


PITCH = randint(PITCH_LOW, PITCH_HIGH)
HUM = randint(HUM_LOW, HUM_HIGH)


class Cricket():

    async def run(self):
        try:
            SND.duty(0)
            await asyncio.sleep(random() * 3 + 1)
            while True:
                t_previous = 0
                self.look()
                self.phase = random()
                self.capacitor = f(self.phase)
                while True:
                    t = ticks_ms() / 1000.0
                    t_elapsed = t - t_previous
                    if t_elapsed >= TICK:
                        interval = abs(t_elapsed - TICK) * 1000
                        if interval > 15:
                            print("jitter", interval)
                        if MOTION and PIR.value():
                            print("MOTION!")
                            LED.off()
                            if STATUS:
                                STS.off()
                            break
                        self.listen()
                        self.phase = min(self.phase + (t_elapsed * FREQ), 1.0)
                        self.capacitor = f(self.phase)
                        if self.capacitor >= 1.0:
                            await self.flash()
                        t_previous = t
                    await asyncio.sleep_ms(1)
        except Exception as e:
            print(e)

    def add_peer(self, peer):
        if peer != mesh.name and peer not in self.recips and len(mesh.peers) < MAX_HOOD:
            print(f"Adding {peer}")
            self.recips[peer] = 0
            mesh.add_peer(peer)

    def remove_peer(self, peer):
        if peer in self.recips:
            print(f"Removing {peer}")
            mesh.remove_peer(peer)
            del self.recips[peer]

    def look(self):
        mesh.group = "null"
        if random() < GROUP_LEADER:
            mesh.group = mesh.name
            print("Group Leader")
        print("Looking for neighbors...")
        SND.duty(512)
        SND.freq(HUM)
        mesh.clear_peers()
        self.recips = {}
        neighbors = mesh.scan()
        if len(neighbors):
            neighbors.sort(key=lambda neighbor: neighbor['rssi'])
            for i in range(INIT_HOOD):
                if i < len(neighbors):
                    peer = neighbors[i]['name']
                    self.add_peer(peer)
        SND.duty(0)
        print("--> done")

    def listen(self):
        while True:
            sender, in_message = mesh.receive()
            if sender is None or in_message is None:
                return
            print("Received", in_message, "from", sender)
            _, sender_group, friend = in_message.split(" ")

            if sender in self.recips:
                self.recips[sender] += 1

            # both unassigned
            if mesh.group == "null" and sender_group == "null":
                self.bump()

            # self unassigned, sender assigned
            elif mesh.group == "null":
                mesh.group = sender_group
                self.add_peer(sender)
                self.bump()

            # self assigned, sender unassigned
            elif sender_group == "null":
                self.add_peer(sender)

            # both have groups assigned
            else:
                if mesh.group == sender_group:
                    self.add_peer(sender)
                    if friend != "null" and random() < FRIEND_LINK:
                        self.add_peer(friend)
                    self.bump()
                else:
                    self.remove_peer(sender)

    def bump(self):
        if self.phase <= REST:
            print("--> resting")
            return
        print("--> bump")
        self.capacitor = min(self.capacitor + BUMP, 1.0)
        self.phase = f_inv(self.capacitor)

    async def flash(self):
        print("--> flash")
        self.phase = 0.0
        if BLINK:
            LED.on()
        if STATUS:
            STS.on()
        if CHIRP:
            SND.duty(512)
            SND.freq(PITCH * 2)
        await asyncio.sleep_ms(30)
        if CHIRP:
            SND.freq(PITCH)
        await asyncio.sleep_ms(120)
        if CHIRP:
            SND.duty(0)
        if BLINK:
            LED.off()
        if STATUS:
            STS.off()
        if len(mesh.peers) < MIN_HOOD:
            self.look()
        else:
            for peer in mesh.peers:
                self.recips[peer] -= 1
                if self.recips[peer] < SEVER:
                    self.remove_peer(peer)
            friend = choice(mesh.peers) if len(mesh.peers) else "null"
            await mesh.send(f"flash {mesh.group} {friend}")
        while True:  # clear any messages
            sender, in_message = mesh.receive()
            if sender is None or in_message is None:
                return


def f(x):
    return math.sin((math.pi / 2) * x)


def f_inv(y):
    return (2 / math.pi) * math.asin(y)





