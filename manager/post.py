from util import *


print()
crickets = scan()
print("CRICKETS:")
for cricket in crickets:
    print(cricket)
print()

filename = "config.py"
filedata = open("config.py").read()

for cricket in crickets:
    try:
        connect(f"ESP_{cricket['name']}")
        response = post_file("http://192.168.4.1/file", filename, filedata)
        print(response)
    except NameError as e:
        print("Request failed:", e)
    sleep(1)
    print()

print("DONE")


"""
curl 192.168.4.1 -F file=@cricket/config.py
"""