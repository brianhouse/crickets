from net import *

network = {}

with open("crickets.json") as f:
    cricket_names = eval(f.read())

i = -1
while len(cricket_names):
    print(json.dumps(cricket_names))
    i += 1
    i %= len(cricket_names)
    cricket_name = cricket_names[i]
    try:
        connect(f"CK_{cricket_name}")
        response = request("http://192.168.4.1/peers")
        print(response)
        if response == "SUCCESS":
            peers = eval("".join(response.split()[1:]))
            network[cricket_name] = peers
            cricket_names.remove(cricket_name)                    
    except Exception as e:
        print("Request failed:", e)
    print()

print("DONE")
print(json.dumps(network))
