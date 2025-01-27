from net import *

print()
crickets = scan()
print("CRICKETS:")
for cricket in crickets:
    print(cricket)
print()

with open("update.txt") as f:
    lines = [line.strip() for line in file]
    filename = lines[0]
    targets = lines[1]
print(f"Posting {filename}...")
print()
filedata = open(filename).read()

for cricket in crickets:
    if len(targets):
        if cricket['name'] not in targets:
            continue
    try:
        connect(f"ESP_{cricket['name']}")
        response = post_file("http://192.168.4.1/file", filename, filedata)
        print(response)
    except Exception as e:
        print("Request failed:", e)
    sleep(1)
    print()

print("DONE")


"""
curl 192.168.4.1 -F file=@cricket/config.py
"""
