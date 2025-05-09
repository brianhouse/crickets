from util import *
from config import *


class Cricket(Node):

    def __init__(self):
        super().__init__()
        SND.duty(0)
        LED.off()
        STS.off()
        self.triggered = False
        O.print(f"## {self.name} ##")

    async def run(self):
        self.t_previous = ticks_ms()
        while True:
            await asyncio.sleep_ms(1)
            t = ticks_ms()
            t_elapsed = ticks_diff(t, self.t_previous)
            if t_elapsed >= TICK:
                self.t_previous = t
                if PIR.value():
                    if not self.triggered:
                        print("TRIGGER")
                        self.triggered = True
                        LED.on()
                        STS.on()
                else:
                    if self.triggered:
                        print("OFF")
                        self.triggered = False
                        LED.off()
                        STS.off()