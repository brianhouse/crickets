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
LED https://www.adafruit.com/product/846  
Piezo https://www.adafruit.com/product/1739  
PIR https://www.adafruit.com/product/5578
Power supply https://www.adafruit.com/product/658  
Power connector https://www.adafruit.com/product/2880  
Resistors https://www.adafruit.com/product/4293  


## Manager

    $ run.py 01E483FC COMMAND

`hello` -- ping crickets for "HELLO WORLD"  
`peers` -- retrieve peer list from all crickets  
`post` -- copy file to all visible crickets  


https://docs.micropython.org/en/latest/reference/mpremote.html  
https://wellys.com/posts/rp2040_mpremote/  


## PIR

Pins are numbered clockwise when looking at the bottom, with #1 being just counter-clockwise from the notch

- Connect pin #1 (SENSE) to ground (most sensitive) - or connect to a resistor divider to decrease sensitivity
- Connect pin #2 (OEN) to 3.3V to turn on / ground to turn off
- Connect pin #3 (VSS) to Ground
- Connect pin #4 (VDD) to 3.3V
- Check signal on pin #5 (REL)
- Connect pin #6 (ONTIME) to ground (min on time of 2 seconds) - or connect a resistor divider to increase up to one hour (3.3v)


ie

- 1: gnd
- 2: 3V
- 3: gnd
- 4: 3v
- 5:   read
- 6: gnd