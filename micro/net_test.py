from esp_helper import *

start_wifi()

print("Looking for neighbors...")
clear_peers()
neighbors = scan()
neighbors.sort(key=lambda n: n['rssi'], reverse=True)
count = 0
for neighbor in neighbors:
    if neighbor['ssid'].split("_")[0] == "ESP" and \
            neighbor['rssi'] > RANGE:
        mac = ap_to_peer(neighbor['mac'])
        print(neighbor['rssi'], neighbor['ssid'], mac)
        add_peer(mac)
        count += 1
        if count == HOOD:
            break
print("--> done")

while True:
    sleep(1)
    print(neighbors)
