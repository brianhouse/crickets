from net import *

with open("crickets.json") as f:
    cricket_names = eval(f.read())

targets = ""
with open("update.txt") as f:
    lines = [line.strip() for line in f]
    filename = lines[0]
print(f"Posting {filename}...")
print()
filedata = open(filename).read()

i = -1
while len(cricket_names):
    print(json.dumps(cricket_names))
    i += 1
    i %= len(cricket_names)
    cricket_name = cricket_names[i]
    try:
        connect(f"CK_{cricket_name}")
        response = post_file("http://192.168.4.1/file", filename, filedata)
        print(response)
        if response == "SUCCESS":
            cricket_names.remove(cricket_name)
    except Exception as e:
        print("Request failed:", e)
    print()


"""
curl 192.168.4.1 -F file=@cricket/config.py
"""
