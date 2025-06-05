# Power

--> check to see if Bluetooth is turned off
https://docs.micropython.org/en/latest/library/bluetooth.html

/

ah! but from a connector standpoint, it's easier to power not off of V+ but off the BAT pin. then I could even solder it. that leaves the FTDI free.

/

V+ is 3.5–6v DC — don't try to use FTDI and a power supply simultaneously!

can tolerate a 1.5v drop from a 5v source (30%) -- but let's say 5%

"ESP32 Active mode current consumption is: (95~240) mA"
LED is 30 mA
Piezo < 10 mA
PIR 123 uA (0.125mA) at 5v

I spec'd 8 10a supplies for 300 crickets, which is ~37 per supply, 270mA available

that's possible. but let's assume 300mA and 9 power supplies w/ 33 each.

each terminal block has 12 ports, so that's 3 each.

makes more sense if it's 36 per supply. I think that's ok. 





height is 14' from floor to ceiling, not rafters
so say 10' (one-way)

5v, 5% drop, 300mA, 10', 80c rated temp

https://www.omnicalculator.com/physics/dc-wire-size

comes back as 25 AWG

22 AWG can get us to 20' (one-way), which is 10' of the ground with 10' of lead in the air


wire:
- https://a.co/d/5orR81N (22 awg)



## Antenna power

wl = network.WLAN()
wl.config(antenna=value)  # 0 internal 1 external
wl.config(txpower=value)  # In dBm


Yes, espnow will just use any txpower setting set in the wifi setup, so network.WLAN(network.STA_IF).config(txpower=17) will set the maximum txpower. (Note due to the wierd mappings used, I believe setting txpower=17 will actually yield a value of 16 due to the actual txpower mappings here (if the docs are correct and I've followed them correctly). Note that micropython mulltiplies the supplied value by 4 and passes that to esp_wifi_set_max_tx_power(). You can check, by calling network.WLAN(network.STA_IF).config("txpower") after setting the value.

https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_wifi.html#_CPPv425esp_wifi_set_max_tx_power6int8_t

put this in config

