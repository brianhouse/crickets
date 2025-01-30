import uasyncio as asyncio
from config import *


class PirTest():

    async def run(self):
        try:
            while True:
                t_previous = 0
                while True:
                    t = ticks_ms() / 1000.0
                    t_elapsed = t - t_previous
                    pir = PIR.value()
                    if pir:
                        LED.on()
                        STS.on()
                        print("MOTION!")
                    else:
                        LED.off()
                        STS.off()
                    t_previous = t
                    await asyncio.sleep_ms(TICK)
        except Exception as e:
            print(e)
