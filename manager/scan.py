import json, time, os
from net import *

EXPECTED = 32


crickets = []
while True:
	for cricket in scan():
		if cricket['name'] not in [cricket['name'] for cricket in crickets]:
			crickets.append(cricket)
			crickets.sort(key=lambda cricket: cricket['rssi'])
			crickets.reverse()
			print("\033c")
			print("CRICKETS:")
			for c, cricket in enumerate(crickets):
				print(c + 1, '\t', cricket['name'], '\t', cricket['rssi'])

	print(".", crickets)
	time.sleep(1)
	if len(crickets) == EXPECTED:
		break


network = {}

for c, cricket in enumerate(crickets):
    print(c + 1)
    try:
        connect(f"CK_{cricket['name']}")
        response = request("http://192.168.4.1/peers")
        print(response)
        peers = eval("".join(response.split()[1:]))
        network[cricket['name']] = peers
        print("--> done")
    except Exception as e:
        print("Request failed:", e)
    sleep(1)
    print()

print("DONE")
print(json.dumps(network))

