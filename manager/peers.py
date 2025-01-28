from net import *

print()
crickets = scan()
print("CRICKETS:")
for cricket in crickets:
    print(cricket)
print()

network = {}

for cricket in crickets:
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
print(network)