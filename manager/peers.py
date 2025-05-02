from net import *

network = {}

with open("crickets.json") as f:
    cricket_names = eval(f.read())

while len(cricket_names):
    print("Remaining:", json.dumps(cricket_names))
    cricket_name = cricket_names.pop()
    try:
        connect(f"CK_{cricket_name}")
        response = request("http://192.168.4.1/peers")
        tokens = response.split()
        group = tokens[1]
        peers = eval(" ".join(tokens[2:]))
        network[cricket_name] = {'group': group, 'peers': peers}            
        print("Network:")
        print(json.dumps(network))
    except Exception as e:
        print("Request failed:", e)
        cricket_names.insert(0, cricket_name)
        print()

print("DONE")
