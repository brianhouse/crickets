# Crickets

ESP32 Huzzah Breakout
https://www.adafruit.com/product/4172
https://learn.adafruit.com/huzzah32-esp32-breakout-board/

FTDI Serial TTL-232 USB Cable
https://www.adafruit.com/product/70

With Arduino
https://learn.adafruit.com/huzzah32-esp32-breakout-board/using-with-arduino-ide

With Micropython
https://micropython.org/download/ESP32_GENERIC/


Before uploading code, put it into bootloader mode by holding down the GPIO #0 button and clicking Reset button, then releasing the #0 button.

## Other Materials
LED https://www.adafruit.com/product/754  <-- need bigger and diffuse
Piezo https://www.adafruit.com/product/1739
PIR https://www.adafruit.com/product/5578  
Power supply https://www.adafruit.com/product/658
Resistors https://www.adafruit.com/product/4293




## Power
https://www.omnicalculator.com/physics/dc-wire-size

V+ is 3.5–6v DC — don't try to use FTDI and a power supply simultaneously!

can tolerate a 1.5v drop from a 5v source (30%) -- but let's say 5%

"ESP32 Active mode current consumption is: (95~240) mA"
LED is 30 mA
Pizeo < 10 mA
PIR 123 uA (0.125mA) at 5v

I spec'd 8 10a supplies for 300 crickets, which is ~37 per supply, 270mA available

that's possible. but let's assume 300mA and 9 power supplies.



--> check to see if Bluetooth is turned off
https://docs.micropython.org/en/latest/library/bluetooth.html


height is 14' from floor to ceiling, not rafters
so say 10', and then double it for the return -- 20'


comes back as 22 AWG, which is great, that's way smaller than my standard 18 awg
https://www.amazon.com/Jacketed-Hookup-Flexible-conductor-Electrical/dp/B081YKFFPW/ref=sr_1_18?crid=C14RSLYI6DML&dib=eyJ2IjoiMSJ9.XEHCaYFh9Z3K5i_ax1Wy5VLRXcVHszUBVh8sI-FwjTgpx3TBdNQf8OBzi-Bb8aY9fRSuj2Tbt3jyZAdZgOTrx24gBELD5L2zvopxYAcla9B1BTvsB9KAqf-kP394D23CujosqD64Y4i08uah9Ykk3ozuX3OUW5i1YNVMXp2B-hOh-pZqzxxvNINFeCXY8OIy3GPMD6bai37CyDrceonYjBdMsLkM3yLSKuzfgY9-6rGtdYxVrZlkN6jdbuIWotI51RoP1bnmJPlgc8P2LXbESmR9yQLt3urwfXGQCuqeecw.b5qNFmgan9638XzqQE7XipOq4DT1xkPn3LZ9WyqqIjs&dib_tag=se&keywords=22+awg+speaker+wire&qid=1722355167&sprefix=22+awg+speaker%2Caps%2C100&sr=8-18


--> need to figure out a plug-in board or something


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
