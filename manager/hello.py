from net import *

print()
crickets = scan()
print("CRICKETS:")
for c, cricket in enumerate(crickets):
    print(c + 1, cricket['name'], cricket['rssi'])
print()

for c, cricket in enumerate(crickets):
    print(c + 1)
    try:
        connect(f"CK_{cricket['name']}")
        response = request("http://192.168.4.1/")
        print(response)
        print("--> done")
    except Exception as e:
        print("Request failed:", e)
    sleep(1)
    print()

print("DONE")