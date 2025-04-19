
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


ESPNow.peers_table


## space

gallery is 70' x 31' 

chop 10' off the front and 6' off all sides

54 x 19 = 1,026 sq ft

1026 / 300 = cricket every 3.42 ft (1.85 x 1.85)

/

studio is 879 sq ft
879 / 3.42 = 257 crickets


point is, 300 is going to be enough


## acrylic

300-35 = 265 / 6 = 44 + 1 = 45

18.50 * 45 = $832.50


## group formation

ok. so making the swap based on distance would be great.

but how do we break week ties?

if a neighbor shares less than X percent ties, cut it


alternately, sending a friend and checking that friend 

having the group assignment in the beginning doesn't solve it, because there can be overlapping groups






