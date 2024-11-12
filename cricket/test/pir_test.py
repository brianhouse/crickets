from esp_helper import *

start_wifi()

while True:
    pir = PIR.value()
    print(pir)
    if pir:
        LED.on()
    else:
        LED.off()
    sleep(.1)