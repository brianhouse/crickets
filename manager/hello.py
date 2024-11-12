from util import *


while True:
    neighbors = scan()
    print("CRICKETS:")
    print(neighbors)
    for neighbor in neighbors:
        connect(f"ESP_{neighbor['name']}".encode('utf-8'))
        print(sta.isconnected())
        try:
            response = request("http://192.168.4.1/")
            print(response)
        except Exception as e:
            print("Request failed:", e)
        sleep(1)
        print()
    print()
    sleep(5)
