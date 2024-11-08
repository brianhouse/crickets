from esp_helper import *
from urequests import get, post

while True:
    neighbors = mesh.scan()
    print("CRICKETS:")
    print(neighbors)
    for neighbor in neighbors:
        mesh.connect(name_to_ssid(neighbor['name']))
        sleep(.5)
        response = get("http://192.168.4.1")
        if response.status_code == 200:
            print(response)
        else:
            print("Error:", response.status_code)
        sleep(1)
        print()
    print()
    sleep(5)


"""
why doesn't this work? it works fine with regular requests

"""
