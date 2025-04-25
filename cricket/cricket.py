import uasyncio as asyncio
from config import *


PITCH = randint(PITCH_LOW, PITCH_HIGH)
HUM = randint(HUM_LOW, HUM_HIGH)


class Cricket():

    async def run(self):
        SND.duty(0)
        await asyncio.sleep(random() * 3 + 1)
        while True:
            t_previous = 0
            self.look()
            self.phase = random()
            self.capacitor = f(self.phase)
            self.looking = False
            self.motion = 0
            while True:
                try:
                    t = ticks_ms() / 1000.0
                    t_elapsed = t - t_previous
                    if t_elapsed >= TICK:
                        # print("TICK", t_elapsed)
                        error = abs(t_elapsed - TICK)
                        if not self.looking and error > .015:
                            self.looking = False
                            print("jitter", error)
                        self.phase = min(self.phase + (t_elapsed * FREQ), 1.0)
                        self.capacitor = f(self.phase)
                        self.listen()
                        if self.capacitor >= 1.0:
                            print('flashing...')
                            await self.flash()
                        if len(mesh.peers) < MIN_HOOD:
                            self.look()
                        if MOTION:
                            if PIR.value():
                                self.motion += 1
                                if self.motion == MOTION:
                                    print("MOTION!")
                                    self.look()
                            else:
                                self.motion -= 1
                                if self.motion < 0:
                                    self.motion = 0
                        t_previous = t
                    await asyncio.sleep_ms(1)
                except Exception as e:
                    print(e)

    def add_peer(self, peer):
        if peer == mesh.name or peer in self.recips:
            return
        # print(f"Adding {peer}")
        mesh.add_peer(peer)
        self.recips[peer] = 0
        mesh.sort_peers()
        if len(mesh.peers) > MAX_HOOD:
            if mesh.get_rssi(mesh.peers[-1]) is not None:
                # print(mesh.peers[-1], "didn't make the cut", mesh.get_rssi(mesh.peers[-1]))
                self.remove_peer(mesh.peers[-1])

    def remove_peer(self, peer):
        if peer in self.recips:
            # print(f"Removing {peer}")
            mesh.remove_peer(peer)
            del self.recips[peer]

    def cull_peers(self):
        for peer in mesh.peers:
            self.recips[peer] -= 1
            if self.recips[peer] <= SEVER:
                # print(peer, "didn't reciprocate")
                self.remove_peer(peer)
        for peer in mesh.peers:
            if mesh.get_rssi(peer) is not None and mesh.get_rssi(peer) < RANGE:
                # print(peer, "is too far")
                self.remove_peer(peer)

    def look(self):
        self.looking = True
        mesh.group = "null"
        if random() < GROUP_LEADER:
            mesh.group = mesh.name
            print("Group Leader")
        print("Looking for neighbors...")
        SND.duty(0)
        SND.duty(512)
        SND.freq(HUM)
        mesh.clear_peers()
        self.recips = {}
        neighbors = mesh.scan()
        if len(neighbors):
            neighbors.sort(key=lambda neighbor: neighbor['rssi'])
            for i in range(MIN_HOOD):
                if i < len(neighbors):
                    peer = neighbors[i]['name']
                    self.add_peer(peer)
        SND.duty(0)
        print("--> done looking")

    def listen(self):
        print("Receiving...")
        while True:
            sender, in_message = mesh.receive()
            if sender is None or in_message is None:
                return
            print("--> received from", sender, ": ", in_message)
            _, sender_group, friend = in_message.split(" ")

            if sender in self.recips.keys():
                self.recips[sender] = 0

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
                print("both")
                if mesh.group == sender_group:
                    print("in group")
                    self.add_peer(sender)
                    # if friend != "null" and random() < FRIEND_LINK:
                    #     self.add_peer(friend)
                    self.bump()
                else:
                    self.remove_peer(sender)

    def bump(self):
        if self.phase <= REST:
            print("--> resting", self.phase)
            return
        self.capacitor = min(self.capacitor + BUMP, 1.0)
        self.phase = f_inv(self.capacitor)
        print("--> bump", self.capacitor)

    async def flash(self):
        print("--> flash")
        self.phase = 0.0
        self.capacitor = 0.0
        if BLINK:
            LED.on()
        if STATUS:
            STS.on()

        self.cull_peers()
        friend = choice(mesh.peers) if len(mesh.peers) else "null"
        print("sending", mesh.peers)
        await mesh.send(f"flash {mesh.group} {friend}")

        if CHIRP:
            SND.duty(512)
            SND.freq(PITCH * 2)
        # await asyncio.sleep_ms(30)
        sleep_ms(30)
        if CHIRP:
            SND.freq(PITCH)
        # await asyncio.sleep_ms(120)
        sleep_ms(30)
        if CHIRP:
            SND.duty(0)
        if BLINK:
            LED.off()
        if STATUS:
            STS.off()


def f(x):
    return math.sin((math.pi / 2) * x)


def f_inv(y):
    return (2 / math.pi) * math.asin(y)







