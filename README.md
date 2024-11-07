# Crickets

ESP32 Huzzah Breakout
https://www.adafruit.com/product/4172
https://learn.adafruit.com/huzzah32-esp32-breakout-board/

FTDI Serial TTL-232 USB Cable
https://www.adafruit.com/product/70

With Micropython
https://micropython.org/download/ESP32_GENERIC/

Before uploading code, put it into bootloader mode by holding down the GPIO #0 button and clicking Reset button, then releasing the #0 button.

## Other Materials
LED https://www.adafruit.com/product/754  <-- need bigger and diffuse
Piezo https://www.adafruit.com/product/1739
PIR https://www.adafruit.com/product/5578  
Power supply https://www.adafruit.com/product/658
Resistors https://www.adafruit.com/product/4293


## Questions

- dynamics of the PIR
    -> seems a bit twitchy — try the version with controls
    https://www.adafruit.com/product/5578    


- large network dynamics
    -> try asymmetrical peering with 3 crickets
    -> check what other peer management functions there are with ESP-now
    (right now I'm just clearing individually — can I clear as a group?)


- lighting
    -> two internal LEDs?

- OTA programming
    -> set the params in a config that survives reboot? show that it's spread?

- housing
    -> ziji


## Design

- turn on the red light when burrring

- a period after motion where it doesn't care about motion (that's a way of making it less sensitive)

- do people carry a battery-powered one in? is that an alternative to the PIR?
  but what triggers them to look around? can that work in the code via timers w/o 
  losing the place in the cycle?

- SUSPENSION
    balllooooonnns!
    pulleys
    anicka li  


## Writing

from the fact of connection to the inherent dynamics of connections itself — nonlinear, unstable
