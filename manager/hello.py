from net import *

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
        response = request("http://192.168.4.1/")
        print(response)
        if response == "SUCCESS":
            cricket_names.remove(cricket_name)
    except Exception as e:
        print("Request failed:", e)
    print()

print("DONE")