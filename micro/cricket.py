from config import *


class Cricket():

    def run(self):
        while True:
            t_previous = 0
            self.look()
            self.phase = random()
            self.capacitor = f(self.phase)
            while True:
                t = ticks_ms() / 1000.0
                t_elapsed = t - t_previous
                if PIR.value():
                    print("MOTION!")
                    LED.off()
                    break
                self.listen()
                self.phase = min(self.phase + (t_elapsed * FREQ), 1.0)
                self.capacitor = f(self.phase)
                if self.capacitor >= 1.0:
                    self.flash()
                t_previous = t
                sleep_ms(TICK)

    def look(self):
        print("Looking for neighbors...")
        SND.duty(512)
        SND.freq(HUM)
        clear_peers()
        neighbors = scan()
        neighbors.sort(key=lambda n: n['rssi'], reverse=True)
        count = 0
        for neighbor in neighbors:
            if neighbor['ssid'].split("_")[0] == "ESP" and \
                    neighbor['rssi'] > RANGE:
                mac = ap_to_peer(neighbor['mac'])
                print(neighbor['rssi'], neighbor['ssid'], mac)
                add_peer(mac)
                count += 1
                if count == HOOD:
                    break
        SND.duty(0)
        print("--> done")

    def listen(self):
        # receive messages
        try:
            sender, in_message = receive()
        except ValueError:
            pass
        else:
            if in_message is not None:
                print("Received", in_message, "from", sender)
                if in_message == "flash":
                    self.bump()
                # setting messages

    def bump(self):
        if self.phase <= REST:
            print("--> resting")
            return
        print("--> bump")
        self.capacitor = min(self.capacitor + BUMP, 1.0)
        self.phase = f_inv(self.capacitor)

    def flash(self):
        print("--> flash")
        self.phase = 0.0
        LED.on()
        SND.duty(512)
        SND.freq(PITCH * 2)
        sleep_ms(20)
        SND.freq(PITCH)
        sleep_ms(20)
        SND.duty(0)
        sleep_ms(50)
        LED.off()
        send("flash")


def f(x):
    return math.sin((math.pi / 2) * x)


def f_inv(y):
    return (2 / math.pi) * math.asin(y)



