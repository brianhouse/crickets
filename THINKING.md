
https://randomnerdtutorials.com/esp32-esp-now-wi-fi-web-server/

https://github.com/orgs/micropython/discussions/12219

//


have a master list of cricket names, and then have the manager functions look for them util they are all uploaded


//

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


## Network

wl = network.WLAN()
wl.config(antenna=value)  # 0 internal 1 external
wl.config(txpower=value)  # In dBm


Yes, espnow will just use any txpower setting set in the wifi setup, so network.WLAN(network.STA_IF).config(txpower=17) will set the maximum txpower. (Note due to the wierd mappings used, I believe setting txpower=17 will actually yield a value of 16 due to the actual txpower mappings here (if the docs are correct and I've followed them correctly). Note that micropython mulltiplies the supplied value by 4 and passes that to esp_wifi_set_max_tx_power(). You can check, by calling network.WLAN(network.STA_IF).config("txpower") after setting the value.

https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_wifi.html#_CPPv425esp_wifi_set_max_tx_power6int8_t

put this in config




## space

call it 
58' x 32' for now

that's 1,856 sq ft

studio is 879 sq ft

that's pretty much half size

artyard grid is at 14.5', clearstory is like 5-10' above that

studio grid is what?


ok, so say 150 crickets for the studio
880/150 = 5.33 sq ft

ha! that's not 5x5, that's 2.5 x 2.5 (but one layer)


so that's the test. 150 on a 2.5 x 2.5 grid in the studio


## plan

so get ziji to build what we know we need now

- 20' wires, 1" of white insulation pulled, 3/16" insulation inner insulation pulled








