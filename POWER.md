# Power

V+ is 3.5–6v DC — don't try to use FTDI and a power supply simultaneously!

can tolerate a 1.5v drop from a 5v source (30%) -- but let's say 5%

"ESP32 Active mode current consumption is: (95~240) mA"
LED is 30 mA
Piezo < 10 mA
PIR 123 uA (0.125mA) at 5v

I spec'd 8 10a supplies for 300 crickets, which is ~37 per supply, 270mA available

that's possible. but let's assume 300mA and 9 power supplies w/ 33 each.

each terminal block has 12 ports, so that's 3 each.





height is 14' from floor to ceiling, not rafters
so say 10' (one-way)

5v, 5% drop, 300mA, 10', 80c rated temp

https://www.omnicalculator.com/physics/dc-wire-size

comes back as 25 AWG

22 AWG can get us to 20' (one-way)




--> check to see if Bluetooth is turned off
https://docs.micropython.org/en/latest/library/bluetooth.html



wire:
- https://a.co/d/0ggxH0D (22 awg)

or
- https://a.co/d/aoXoifs (24 awg)



/

ah! but from a connector standpoint, it's easier to power not off of V+ but off the BAT pin. then I could even solder it. that leaves the FTDI free.