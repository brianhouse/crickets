from net import *

print()
crickets = scan()
print("CRICKETS:")
for cricket in crickets:
    print(cricket)
print()

targets = ""
with open("update.txt") as f:
    lines = [line.strip() for line in f]
    filename = lines[0]
    if len(lines) > 1:
        targets = lines[1].split()
print(f"Posting {filename}...")
print()
filedata = open(filename).read()

failed = []

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
        failed.append(cricket['name'])
    sleep(1)
    print()

print("DONE")
print("Failed:")
for name in failed:
    print(name)


"""
curl 192.168.4.1 -F file=@cricket/config.py
"""
