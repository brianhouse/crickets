import uasyncio as asyncio
from config import *


PITCH = randint(PITCH_LOW, PITCH_HIGH)
HUM = randint(HUM_LOW, HUM_HIGH)


class Cricket():

    async def run(self):
        try:
            await asyncio.sleep(random() + 2)
            while True:
                t_previous = 0
                self.look()
                self.phase = random()
                self.capacitor = f(self.phase)
                while True:
                    t = ticks_ms() / 1000.0
                    t_elapsed = t - t_previous
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
                    await asyncio.sleep_ms(TICK)
        except Exception as e:
            print(e)

    def look(self):
        print("Looking for neighbors...")
        SND.duty(512)
        SND.freq(HUM)
        mesh.clear_peers()
        count = 0
        for neighbor in mesh.scan():
            neighbor, rssi = neighbor.values()
            if rssi > RANGE:
                print(neighbor)
                mesh.add_peer(neighbor)
                count += 1
                if count == HOOD:
                    break
        SND.duty(0)
        print("--> done")

    def listen(self):
        sender, in_message = mesh.receive()
        if in_message is not None:
            print("Received", in_message, "from", sender)
            if in_message == "flash":
                if len(mesh.peers) < HOOD and sender not in mesh.peers:
                    print("Adding", sender)
                    mesh.add_peer(sender)
                self.bump()

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
            sleep_ms(80)
            SND.freq(PITCH)
            sleep_ms(20)
            SND.duty(0)
            sleep_ms(50)
        if BLINK:
            LED.off()
        if STATUS:
            STS.off()
        await mesh.send("flash")


def f(x):
    return math.sin((math.pi / 2) * x)


def f_inv(y):
    return (2 / math.pi) * math.asin(y)





