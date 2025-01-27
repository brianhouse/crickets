from net import *

print()
crickets = scan()
print("CRICKETS:")
for cricket in crickets:
    print(cricket)
print()

for cricket in crickets:
    try:
        connect(f"ESP_{cricket['name']}")
        response = request("http://192.168.4.1/")
        print(response)
        print("--> done")
    except Exception as e:
        print("Request failed:", e)
    sleep(1)
    print()

print("DONE")