from esp_helper import *
from urequests import get, post

while True:
    neighbors = mesh.scan()
    print("CRICKETS:")
    print(neighbors)
    for neighbor in neighbors:
        mesh.connect(name_to_ssid(neighbor['name']))
        #r = get("http://192.168.4.1:8088/peers")
        #print(r.text)
        sleep(1)
        print()
    print()
    sleep(5)



