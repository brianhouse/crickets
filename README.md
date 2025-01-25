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
PIR https://www.adafruit.com/product/5578  (missing 150)  
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


## Cricket