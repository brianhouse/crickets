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
Resistors https://a.co/d/iYcJ9PN
Speaker Wire https://www.amazon.com/dp/B099P8TZD6
Acrylic https://shop.glowforge.com/products/clear-acrylic-cast-transparent-glossy?variant=39434532323426

## Manager

    $ run.py 01E483FC COMMAND

`scan` -- find reachable crickets for crickets.json used in other commands
`hello` -- ping for "HELLO WORLD"  
`peers` -- retrieve peer list
`post [file]` -- copy file
`resume` -- start normal behavior after pause/upload
`reset` -- soft reset of cricket
`map` -- pause with light for 8 seconds and then resume


## PIR

Pins are numbered clockwise when looking at the bottom, with #1 being just counter-clockwise from the notch

- Connect pin #1 (SENSE) to ground (most sensitive) - or connect to a resistor divider to decrease sensitivity
- Connect pin #2 (OEN) to 3.3V to turn on / ground to turn off
- Connect pin #3 (VSS) to Ground
- Connect pin #4 (VDD) to 3.3V
- Check signal on pin #5 (REL)
- Connect pin #6 (ONTIME) to ground (min on time of 2 seconds) - or connect a resistor divider to increase up to one hour (3.3v)

ie
- 1:   knob
- 2: 3V
- 3: gnd
- 4: 3v
- 5:   read
- 6: gnd

