from esp_helper import *

# connection constants
RANGE = -100
HOOD = 5

# capacitor constants
FREQ = 1            # endogenous frequency in Hz
BUMP = 0.01         # capacitor bump amount when neighbor flashes
REST = 0.1          # percent of cycle to be unresponsive after flash
TICK = 1            # cycle resolution in ms

# automatic constants
PITCH = randint(3500, 4500)


# have a mode for just PIR testing

start_wifi()


class Cricket():

    def __init__(self):
        self.phase = random()
        self.capacitor = f(self.phase)

    def run(self):
        t_previous = 0
        self.look()
        while True:
            t = ticks_ms() / 1000.0
            t_elapsed = t - t_previous
            self.listen()
            self.phase = min(self.phase + (t_elapsed * FREQ), 1.0)
            self.capacitor = f(self.phase)
            if self.capacitor >= 1.0:
                self.flash()
            t_previous = t
            sleep_ms(TICK)

    def look(self):
        print("Looking for neighbors...")
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

    def listen(self):
        # receive messages
        sender, in_message = receive()
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


cricket = Cricket()
cricket.run()

