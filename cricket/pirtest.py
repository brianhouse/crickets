from util import *
from config import *


class Cricket(Node):

    def __init__(self):
        super().__init__()
        SND.duty(0)
        LED.off()
        STS.off()
        self.motion = 0
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
                        self.motion = 0
                        self.triggered = True
                        print("TRIGGER")
                        LED.on()
                        STS.on()
                    self.motion += 1
                else:
                    if self.triggered:
                        self.triggered = False
                        print("OFF")
                        LED.off()
                        STS.off()
                # print(self.motion)
                # if PIR.value():
                #     print("MOTION")
                #     self.motion += 1
                #     if self.motion >= MOSENS:
                #         print("TRIGGER")
                #         self.motion = 0
                #         await self.look()
                #         continue
                # else:
                #     self.motion = 0
