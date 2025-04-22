from net import *

with open("crickets.json") as f:
    cricket_names = eval(f.read())

while len(cricket_names):
    print(json.dumps(cricket_names))
    cricket_name = cricket_names.pop()
    try:
        connect(f"CK_{cricket_name}")
        response = request("http://192.168.4.1/")
        print(response)
    except Exception as e:
        print("Request failed:", e)
        cricket_names.insert(0, cricket_name)        
    print()

print("DONE")